import json
from urllib.request import Request, urlopen
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from dal import autocomplete
from .models import UserTopList, Category, Object, UserProfile
from .forms import ChoicesForm
from recommender.views import recommender
from recommender.models import RecommendationList, UserLikeList, UserDislikeList

# Create your views here.
def home(request):
    return render(request, 'projectl/home.html')

class edit_autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Object.objects.none()

        category = Category.objects.get(pk=self.request.session['category'])

        #something happens with id = 0
        qs = Object.objects.all().exclude(pk=0).filter(category=category).order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q, category=category)

        return qs

@login_required
def edit(request, category):
    request.session['category'] = category
    list_category = Category.objects.get(pk=category)
    user = request.user.profile

    if request.method == 'POST':
        choices_form = ChoicesForm(request.POST)
        if choices_form.is_valid():
            choices = []
            try:
                choices.append(Object.objects.get(name=choices_form.cleaned_data['choice_1']))
            except:
                pass
            try:
                choices.append(Object.objects.get(name=choices_form.cleaned_data['choice_2']))
            except:
                pass
            try:
                choices.append(Object.objects.get(name=choices_form.cleaned_data['choice_3']))
            except:
                pass
            try:
                choices.append(Object.objects.get(name=choices_form.cleaned_data['choice_4']))
            except:
                pass
            try:
                choices.append(Object.objects.get(name=choices_form.cleaned_data['choice_5']))
            except:
                pass

            # Delete previous Top List
            prev_top_list = UserTopList.objects.filter(user=user, category=list_category).delete()

            # Add new Top List
            # Also add Top choice to Like List and/or delete from Dislike List
            for choice in choices:
                top_object = UserTopList.create(object=choice, user=user, category=list_category).save()

                if UserLikeList.objects.filter(user=user, object=choice).count() == 0:
                    like_object = UserLikeList.create(object=choice, user=user, category=list_category).save()

                dislike_object = UserDislikeList.objects.filter(user=user, object=choice).delete()

            recommender(request, category)
            return render(request, 'lists/edit_success.html', {'category': list_category})
    else:
        prev_top_list = UserTopList.objects.filter(user=user, category=list_category)
        it = 0
        choices = []
        for choice in prev_top_list:
            choices.append(choice.object)
            it+=1
        while it < 5:
            choices.append(None)
            it+=1
        choice_1 = choices[0]
        choice_2 = choices[1]
        choice_3 = choices[2]
        choice_4 = choices[3]
        choice_5 = choices[4]
        choices_form = ChoicesForm(initial={'choice_1': choice_1, 'choice_2': choice_2, 'choice_3': choice_3, 'choice_4': choice_4, 'choice_5': choice_5})

    url_reverse = reverse('edit', args=[list_category.pk])

    return render(request, 'lists/edit.html', {'form': choices_form, 'category': list_category, 'url_reverse': url_reverse})

@login_required
def get_user_friends(request):
	friends = []
	if request.user.is_authenticated():
		social_user = request.user.social_auth.filter(
    		provider='facebook',
			).first()
		if social_user:
				url = u'https://graph.facebook.com/{0}/' \
      			u'friends?fields=id,name' \
      			u'&access_token={1}'.format(
          			social_user.uid,
          			social_user.extra_data['access_token'],
      			)
				request = Request(url)
				friends = json.loads(urlopen(request).read().decode('utf-8')).get('data')
	return [friend['id'] for friend in friends]

@login_required
def user_list(request, category):

    user_choices = UserTopList.objects.filter(user=request.user.profile, category__nav_url_slug=category)
    recommendations = RecommendationList.objects.filter(user=request.user.profile, category__nav_url_slug=category)
    user_dislikes = UserDislikeList.objects.filter(user=request.user.profile, category__nav_url_slug=category)
    choices = []
    for choice in user_choices:
        choices.append(choice.object)
    user_likes = UserLikeList.objects.filter(user=request.user.profile, category__nav_url_slug=category).exclude(object__in=choices)

    list_category = Category.objects.get(nav_url_slug=category)

    friends_profile = UserProfile.objects.filter(fbid__in = get_user_friends(request))

    user_recommendations = {}
    for rec in recommendations:
        user_recommendations[rec.object] = UserTopList.objects.filter(object=rec.object).filter(user__in = friends_profile).exclude(user=request.user.profile).first()

    unanswered_categories = []
    all_categories = Category.objects.order_by('name')

    return render(request, 'lists/user_list.html', {'user_likes': user_likes, 'user_dislikes': user_dislikes, 'user_recommendations': user_recommendations, 'user_choices': user_choices, 'all_categories': all_categories, 'unanswered_categories': unanswered_categories, 'list_category': list_category, 'active_nav':category})

@login_required
def all_categories(request):

    user_choices = UserTopList.objects.filter(user=request.user.profile)

    answered_categories = set()
    for choice in user_choices:
        if choice.category not in answered_categories:
            answered_categories.add(choice.category)

    unanswered_categories = Category.objects.exclude(name__in = answered_categories)

    all_categories = Category.objects.order_by('name')

    return render(request, 'lists/all_categories.html', {'answered_categories': answered_categories, 'unanswered_categories': unanswered_categories, 'all_categories': all_categories, 'active_nav':'all'})

@login_required
def profile(request, user_id):

    isMyProfile = False

    if UserProfile.objects.filter(fbid__in = get_user_friends(request)).filter(pk=user_id).count() == 0:
        # user_id is either User or Stranger
        if user_id == str(request.user.id):
            # user_id is for User
            isMyProfile = True

        else:
            # user_id is stranger's
            return redirect('all_categories')

    user = UserProfile.objects.get(user=user_id)
    top_choices = UserTopList.objects.filter(user=user_id)
    answered_categories = Category.objects.filter(usertoplist__in=top_choices).distinct()

    categories_and_choices = {}
    for category in answered_categories:
        categories_and_choices[category] = top_choices.filter(category=category)

    if isMyProfile:
        return render(request, 'lists/user_profile.html', {'categories_and_choices': categories_and_choices, 'user': user})
    else:
        return render(request, 'lists/user_profile.html', {'categories_and_choices': categories_and_choices, 'user': user})

# MIGHT USE IN THE FUTURE
'''
@login_required
def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('all_categories')
    else:
        form = EmailForm()
    return render(request, 'projectl/email.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
    '''
