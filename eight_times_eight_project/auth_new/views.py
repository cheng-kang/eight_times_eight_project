from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from eight_times_eight_project.auth_new.forms import SignUpForm,SignUpProfileForm
from django.contrib.auth.models import User
from eight_times_eight_project.auth_new.models import Profile
from eight_times_eight_project.feeds.models import Feed

def signup(request):
    if request.method == 'POST':
        userForm = SignUpForm(request.POST)
        profileForm = SignUpProfileForm(request.POST)
        if not userForm.is_valid() or not profileForm.is_valid():
            return render(request, 'auth_new/signup.html', {'userForm': userForm, 'profileForm':profileForm})
        else:
            username = userForm.cleaned_data.get('username')
            email = userForm.cleaned_data.get('username')
            password = userForm.cleaned_data.get('password')
            realname = profileForm.cleaned_data.get('realname')
            major = profileForm.cleaned_data.get('major')
            enter_year = profileForm.cleaned_data.get('enter_year')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)

            user.profile.realname = realname
            user.profile.major = major
            user.profile.enter_year = enter_year


            user.save()

            login(request, user)
            welcome_post = u'{0} has joined the network.'.format(user.username, user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()
            return redirect('/')
    else:
        return render(request, 'auth_new/signup.html', {'userForm': SignUpForm(), 'profileForm': SignUpProfileForm()})
