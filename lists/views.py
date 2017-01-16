from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from .models import Choice, UserProfile, Category
from .forms import EmailForm, ChoiceForm
# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def submit_choice(request):
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            user = request.user.profile
            choice_object = Choice.create(name=choice, user=user)
            choice_object.save()
            return redirect('user_list')
    else:
        form = ChoiceForm()
    return render(request, 'core/choose_category.html', {'form': ChoiceForm})

'''
@login_required
def choose_category(request):    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            request.session['category'] = category.name
            return redirect('submit_lists')
    else:
        form = CategoryForm()
    return render(request, 'core/choose_category.html', {'form': form})
    

@login_required
def submit_lists(request):
    cat_name = request.session.get('category')
    category = Category.objects.filter(name = cat_name)
    if request.method == 'POST':
        form = ListForm(request.POST, category=category)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            user = request.user.profile
            Choice.objects.create(name=choice, user=user)
            return redirect('user_list')
    else:
        form = ListForm(category=category)
    return render(request, 'core/submit_lists.html', {'form': form, 'category': cat_name})
'''

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
