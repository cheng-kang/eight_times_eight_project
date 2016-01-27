# -*- coding: UTF-8 -*-

import os
from PIL import Image

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings as django_settings
from django.shortcuts import render, redirect, get_object_or_404

from eight_times_eight_project.core.forms import ProfileForm, ChangePasswordForm
from eight_times_eight_project.feeds.models import Feed
from eight_times_eight_project.feeds.views import FEEDS_NUM_PAGES
from eight_times_eight_project.feeds.views import feeds
from eight_times_eight_project.auth_new.models import Profile


def home(request):

    if request.user:
        user = request.user
    else:
        user = None

    profiles = Profile.objects.all().order_by("votes")[:8]
    return render(request, 'core/index.html', {'users':profiles, "user": user })

@login_required
def network(request):
    users_list = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'core/network.html', { 'users': users })


def profile(request, id):

    if request.user:
        user = request.user
    else:
        user = None

    page_user = get_object_or_404(User, pk=id)

    return render(request, 'core/profile.html', {
        'page_user': page_user,
        'user': user,
        })

@login_required
def me(request):
    user = request.user

    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True
    except Exception, e:
        pass

    profile_form = ProfileForm(instance=user)
    change_password_form = ChangePasswordForm(instance=user)

    return render(request, 'core/me.html', {'user':user, 'profile_form':profile_form, 'change_password_form':change_password_form, 'uploaded_picture': uploaded_picture})

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user.profile.realname = profile_form.cleaned_data.get('realname')
            gender = profile_form.cleaned_data.get('gender')
            if gender is not 'm' or gender is not 'f':
                gender = 'm'
            user.profile.gender = gender
            user.profile.major = profile_form.cleaned_data.get('major')
            user.profile.enter_year = profile_form.cleaned_data.get('enter_year')
            user.profile.wechat = profile_form.cleaned_data.get('wechat')
            user.profile.phone = profile_form.cleaned_data.get('phone')
            user.email = profile_form.cleaned_data.get('email')
            user.profile.address = profile_form.cleaned_data.get('address')
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile were successfully edited.')
    else:
        messages.add_message(request, messages.SUCCESS, 'Something went wrong.')

    return redirect('/me/')

@login_required
def update_password(request):
    user = request.user
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            new_password = change_password_form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your password were successfully changed.')
    else:
        messages.add_message(request, messages.SUCCESS, 'Something went wrong.')
    return redirect('/me/')


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True
    except Exception, e:
        pass
    return render(request, 'core/picture.html', {'uploaded_picture': uploaded_picture})


@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)    
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)
        return redirect('/me/?upload_picture=uploaded')
    except Exception, e:
        return redirect('/me/')

@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
    except Exception, e:
        pass
    return redirect('/me/')