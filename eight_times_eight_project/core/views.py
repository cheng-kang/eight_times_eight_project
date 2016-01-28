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
from eight_times_eight_project.decorators import ajax_required

from eight_times_eight_project.activities.models import Activity, Notification
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from eight_times_eight_project.messages_new.models import Message

def home(request):

    if request.user:
        user = request.user

        friends = Activity.objects.filter(activity_type=Activity.CONFIRM_FRIEND, to_user=user.pk)
        friend_id_list = []
        for item in friends:
            friend_id_list.append(item.user.pk)

        pending_friends = Activity.objects.filter(activity_type=Activity.ADD_FRIEND, user=user)
        pending_friend_id_list = []
        for item in pending_friends:
            pending_friend_id_list.append(item.to_user)

        voted = Activity.objects.filter(activity_type=Activity.VOTE, user=user)
        voted_id_list = []
        for item in voted:
            voted_id_list.append(item.to_user)

        print user.pk,user.pk.__doc__ in voted_id_list

        print friend_id_list,pending_friend_id_list,voted_id_list


    else:
        user = None
        friend_id_list = None
        pending_friend_id_list = None
        voted_id_list = None

    profiles = Profile.objects.all().order_by("votes")[:8]
    return render(request, 'core/index.html', {'users':profiles,
                                               "user": user,
                                               'friend_id_list': friend_id_list,
                                               'pending_friend_id_list': pending_friend_id_list,
                                               'voted_id_list': voted_id_list,
                                               })

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

        friends = Activity.objects.filter(activity_type=Activity.CONFIRM_FRIEND, to_user=user.pk)
        friend_id_list = []
        for item in friends:
            friend_id_list.append(item.user.pk)

        pending_friends = Activity.objects.filter(activity_type=Activity.ADD_FRIEND, user=user)
        pending_friend_id_list = []
        for item in pending_friends:
            pending_friend_id_list.append(item.to_user)

        voted = Activity.objects.filter(activity_type=Activity.VOTE, user=user)
        voted_id_list = []
        for item in voted:
            voted_id_list.append(item.to_user)


    else:
        user = None
        friend_id_list = None
        pending_friend_id_list = None
        voted_id_list = None

    page_user = get_object_or_404(User, pk=id)

    return render(request, 'core/profile.html', {
        'page_user': page_user,
        'user': user,
       'friend_id_list': friend_id_list,
       'pending_friend_id_list': pending_friend_id_list,
       'voted_id_list': voted_id_list,
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
def friends(request):
    user = request.user

    friends = Activity.objects.filter(activity_type=Activity.CONFIRM_FRIEND, to_user=user.pk)

    return render(request, 'core/friends.html', {'user':user, 'friends': friends})

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


@login_required
@ajax_required
def vote(request):
    user = request.user
    vote_id = request.POST['vote']
    print vote_id,user.pk,str(vote_id)==str(user.pk)
    if str(vote_id)==str(user.pk):
        return HttpResponse("cant")
    else:
        to_user = User.objects.get(pk=vote_id)
        vote = Activity.objects.filter(activity_type=Activity.VOTE, to_user=vote_id, user=user)
        if vote:
            to_user.profile.votes -= 1
            to_user.save()
            user.profile.unotify_voted(to_user)
            vote.delete()
        else:
            vote = Activity(activity_type=Activity.VOTE, to_user=vote_id, user=user)
            vote.save()
            to_user.profile.votes += 1
            to_user.save()
            user.profile.notify_voted(to_user)
        return HttpResponse(to_user.profile.votes)

@login_required
@ajax_required
def add_friend(request):
    user = request.user
    user_id = request.POST['user_id']
    print str(user_id)==str(user.pk),user_id,user.pk
    if str(user_id)==str(user.pk):
        return HttpResponse("cant")
    else:
        to_user = User.objects.get(pk=user_id)
        user = request.user
        friend = Activity.objects.filter(activity_type=Activity.ADD_FRIEND, to_user=user_id, user=user)

        m = ""
        if friend:
            user.profile.unotify_added(to_user)
            # to_user.profile.notify_added(user)
            friend.delete()
            m = "cancel"
        else:
            friend = Activity(activity_type=Activity.ADD_FRIEND, to_user=user_id, user=user)
            friend.save()
            user.profile.notify_added(to_user)
            m = "sent"
        return HttpResponse(m)

# 此函数逻辑与发送好友申请函数逻辑略有不同
@login_required
@ajax_required
def confirm_friend(request):
    user_id = request.POST['user_id']
    to_user = User.objects.get(pk=user_id)
    user = request.user
    friend = Activity.objects.filter(activity_type=Activity.ADD_FRIEND, to_user=user.pk, user=to_user)

    m = ""
    # 如果存在该好友申请activity,则将其修改为确认好友activity,并添加当前用户确认好友activity
    if friend:
        friend.update(activity_type=Activity.CONFIRM_FRIEND)

        new_friend = Activity(activity_type=Activity.CONFIRM_FRIEND, to_user=user_id, user=user)
        new_friend.save()
        # 给双方好友数 +1 并保存
        to_user.profile.friends += 1
        to_user.save()
        user.profile.friends += 1
        user.save()

        # 发送好友添加成功通知
        user.profile.notify_confirmed(to_user)
        to_user.profile.notify_confirmed(user)
        to_user.profile.unotify_added(user)

        Message.send_message(user, to_user, "我们成为好友了。")

        m = "ok"
    # 如不存在则报错
    else:
        m = "wrong"
    return HttpResponse(m)

@login_required
@ajax_required
def remove_friend(request):
    user_id = request.POST['user_id']
    to_user = User.objects.get(pk=user_id)
    user = request.user
    friend = Activity.objects.filter(activity_type=Activity.CONFIRM_FRIEND, to_user=user.pk, user=to_user)

    # 删除该activity
    if friend:
        friend.delete()

        # 给双方好友数 -1 并保存
        to_user.profile.friends -= 1
        to_user.save()

    # 同上对该好友进行操作
    friend = Activity.objects.filter(activity_type=Activity.CONFIRM_FRIEND, to_user=user_id, user=user)

    if friend:
        friend.delete()

        user.profile.friends -= 1
        user.save()

    # 发送好友删除成功通知
    # user.profile.notify_removed(to_user)
    # to_user.profile.notify_removed(user)

    return HttpResponse("removed")

@login_required
@ajax_required
def decline_friend(request):
    user_id = request.POST['user_id']
    to_user = User.objects.get(pk=user_id)
    user = request.user
    friend = Activity.objects.filter(activity_type=Activity.ADD_FRIEND, to_user=user.pk, user=to_user)

    # 删除该activity
    if friend:
        friend.delete()

    # 发送通知
    user.profile.notify_declined(to_user)
    to_user.profile.unotify_added(user)

    return HttpResponse("declined")
