from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from dal import autocomplete
from social_django.models import UserSocialAuth
from .models import UserChoiceList, Category, Object
from .forms import EmailForm, ChoicesForm

# Create your views here.
def home(request):
    return render(request, 'projectl/home.html')


class edit_autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Country.objects.none()

        category = Category.objects.get(pk=self.request.session['category'])

        #something happens with id = 0
        qs = Object.objects.all()
        qs = Object.objects.exclude(pk=0)

        if self.q:
            qs = qs.filter(name__istartswith=self.q, category=category)

        return qs

@login_required
def edit(request, category):
    request.session['category'] = category
    list_category = Category.objects.get(pk=category)
    user = request.user.profile

    if request.method == 'POST':
        choices_form = ChoicesForm(request.POST)
        if choices_form.is_valid():
            try:
                choice_1 = Object.objects.get(name=choices_form.cleaned_data['choice_1'])
            except:
                choice_1 = None
            try:
                choice_2 = Object.objects.get(name=choices_form.cleaned_data['choice_2'])
            except:
                choice_2 = None
            try:
                choice_3 = Object.objects.get(name=choices_form.cleaned_data['choice_3'])
            except:
                choice_3 = None
            try:
                choice_4 = Object.objects.get(name=choices_form.cleaned_data['choice_4'])
            except:
                choice_4 = None
            try:
                choice_5 = Object.objects.get(name=choices_form.cleaned_data['choice_5'])
            except:
                choice_5 = None

            user_list = UserChoiceList.objects.filter(user=user, category=list_category)
            if user_list.count() > 0:
                user_list.update(choice_1=choice_1, choice_2=choice_2, choice_3=choice_3, choice_4=choice_4, choice_5=choice_5)
            else:
                list_object = UserChoiceList.create(choice_1=choice_1, choice_2=choice_2, choice_3=choice_3, choice_4=choice_4, choice_5=choice_5, user=user)
                list_object.save()
            return render(request, 'lists/edit_success.html', {'category': list_category})
    else:
        user_list = UserChoiceList.objects.filter(user=user, category=list_category)
        if user_list.count() > 0:
            prev_list = user_list.first()
            choices_form = ChoicesForm(initial={'choice_1': prev_list.choice_1, 'choice_2': prev_list.choice_2,
                        'choice_3': prev_list.choice_3, 'choice_4': prev_list.choice_4, 'choice_5': prev_list.choice_5})
        else:
            choices_form = ChoicesForm()

    url_reverse = reverse('edit', args=[list_category.pk])

    return render(request, 'lists/edit.html', {'form': choices_form, 'category': list_category, 'url_reverse': url_reverse})

@login_required
def user_list(request):

    if request.user.email=="":
        return redirect('email')

    user_choices = UserChoiceList.objects.filter(user=request.user.profile)
    answered_categories = []
    for list in user_choices:
        answered_categories.append(list.category)

    unanswered_categories = Category.objects.exclude(name__in = answered_categories)

    return render(request, 'lists/user_list.html', {'user_choices': user_choices, 'unanswered_categories': unanswered_categories})

@login_required
def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('user_list')
    else:
        form = EmailForm()
    return render(request, 'projectl/email.html', {'form': form})

# MIGHT USE IN THE FUTURE
'''
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
