from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from .models import Choice, UserProfile, Category, Object
from .forms import EmailForm, ChoicesForm, CategoryForm
# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def submit_choice(request):

    user = request.user.profile

    if 'category' not in request.session:
        request.session['category'] = 'Restaurants'    

    category = Category.objects.get(name=request.session['category'])

    if request.method == 'POST':
        if 'category' in request.POST: 
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category = category_form.cleaned_data['category']
                request.session['category'] = category.name
                user_list = Choice.objects.filter(user=user, category=category)
                if user_list.count() > 0:
                    prev_list = user_list.first()
                    choices_form = ChoicesForm(initial={'choice_1': prev_list.choice_1, 'choice_2': prev_list.choice_2, 'choice_3': prev_list.choice_3,
                                                'choice_4': prev_list.choice_4, 'choice_5': prev_list.choice_5})
                else:
                    choices_form = ChoicesForm()
        elif 'choices' in request.POST: 
            choices_form = ChoicesForm(request.POST)
            if choices_form.is_valid():
                choice_1 = choices_form.cleaned_data['choice_1']
                choice_2 = choices_form.cleaned_data['choice_2']
                choice_3 = choices_form.cleaned_data['choice_3']
                choice_4 = choices_form.cleaned_data['choice_4']
                choice_5 = choices_form.cleaned_data['choice_5']

                user_list = Choice.objects.filter(user=user, category=category)
                if user_list.count() > 0: 
                    user_list.update(choice_1=choice_1, choice_2=choice_2, choice_3=choice_3, choice_4=choice_4, choice_5=choice_5)
                else:
                    list_object = Choice.create(choice_1=choice_1, choice_2=choice_2, choice_3=choice_3, choice_4=choice_4, choice_5=choice_5, user=user)
                    list_object.save()
    else:
        user_list = Choice.objects.filter(user=user, category=category)
        if user_list.count() > 0:
            prev_list = user_list.first()
            choices_form = ChoicesForm(initial={'choice_1': prev_list.choice_1, 'choice_2': prev_list.choice_2, 'choice_3': prev_list.choice_3,
                                                'choice_4': prev_list.choice_4, 'choice_5': prev_list.choice_5})
        else:
            choices_form = ChoicesForm()
        

    category = Category.objects.get(name=request.session['category'])
    category_form = CategoryForm(initial={'category': category})
    choices_form.fields['choice_1'].queryset = Object.objects.filter(category=category)
    choices_form.fields['choice_2'].queryset = Object.objects.filter(category=category)
    choices_form.fields['choice_3'].queryset = Object.objects.filter(category=category)
    choices_form.fields['choice_4'].queryset = Object.objects.filter(category=category)
    choices_form.fields['choice_5'].queryset = Object.objects.filter(category=category)

    return render(request, 'core/submit_choice.html', {'category_form': category_form, 'choices_form': choices_form })

@login_required
def user_list(request):

    if request.user.email=="":
        return redirect('email')
    
    user_choices = Choice.objects.filter(user=request.user.profile)
    
    return render(request, 'lists/user_list.html', {'user_choices': user_choices})

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
    return render(request, 'registration/email.html', {'form': form})

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
