from django.shortcuts import get_object_or_404, render

# Create your views here.

# for login and signup and more
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from hobbies.forms import LoginForm, SignupForm
from hobbies.models import FriendList, User, Profile, Hobby

from django.http import JsonResponse


def members_view(request):
    return render(request, 'hobbies/pages/members.html')

def profile_view(request):
    return render(request, 'hobbies/pages/profile.html')

def redirectLogin(request):
    if request.user.is_authenticated:
        return (redirect('/members'))
    return (redirect('/login'))


def signup(request):
    uservalue=''
    passwordvalue1=''
    if request.user.is_authenticated:
        return (redirect('/members'))

    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST) 
        if form.is_valid():
            
            uservalue = form.cleaned_data['username']
            passwordvalue1 = form.cleaned_data['password']
           
           # Here we do comparision to check if username exists 
            try:
                user= User.objects.get(username=uservalue)  
                return render(request, 'hobbies/error.html', {
                'error' : 'The username you entered has already been taken. Please try another username.'
            })
            except User.DoesNotExist:
                
                             #create a profile
                    new_profile = Profile.objects.create(profile_username=uservalue)
                    new_profile.save()
                    # create a new user
                    new_user = User.objects.create(username=uservalue, profile=new_profile)

                    # set user's password
                    new_user.set_password(passwordvalue1)
                    new_user.save()

                    newFriendList = FriendList.objects.create(user = new_user)
                    newFriendList.save()
         
                    # authenticate user
                    # establishes a session, will add user object as attribute
                    # on request objects, for all subsequent requests until logout
                    user = auth.authenticate(username=uservalue, password=passwordvalue1)
                    if user is not None:
                        auth.login(request, user)
                        return redirect('hobbies:members')

    return render(request, 'hobbies/auth/signup.html', { 'form': SignupForm })

def login(request):

    if request.user.is_authenticated:
        return (redirect('/members'))

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('hobbies:members')

            # failed authentication   This is added change
            return render(request, 'hobbies/error.html', {
                'error' : 'User not registered. Sign up first or Wrong Password'
            })

        # invalid form
        return render(request, 'hobbies/auth/login.html', {
            'form': form
        })

    return render(request, 'hobbies/auth/login.html', { 'form': form })
@login_required
def logout(request):
    auth.logout(request)
    return redirect('hobbies:login')


# still thinking about this one 
def view_profile(request, view_username):
    '''This  if when account is already created or does not exist'''
    
    username = request.user.username
    greeting = "Your" if username == view_username else view_username + "'s"
    try:
       user = User.objects.get(username=view_username)
    except User.DoesNotExist:
       context = {
          'error' : 'User ' + view_username + ' does not exist'
       }
       return render(request, 'hobbies/error.html', context)
    context = {
        'view_user': view_username,
        'greeting': greeting,
        'profile': user.profile,
    }
    return render(request, 'hobbies/pages/member.html', context)

@login_required
def members(request):
    user = request.user

    return render(request, 'hobbies/pages/members.html', {
            'page': 'members',
            'user': user,
            'members': User.objects.exclude(username=user.username),
    })



