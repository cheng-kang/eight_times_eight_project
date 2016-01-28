from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from eight_times_eight_project.feeds.models import Feed
from django.contrib.auth.decorators import login_required
from eight_times_eight_project.auth_new.models import Profile
from eight_times_eight_project.activities.models import Activity

@login_required
def search(request):

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

    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')
        
        count = 0

        results = Profile.objects.filter(Q(realname__icontains=querystring) | Q(major__icontains=querystring) | Q(enter_year__icontains=querystring))

        count = results.count()

        return render(request, 'search/search.html', {
            'hide_search': True,
            'querystring': querystring,
            'count': count,
            'results': results,
            'user': user,
           'friend_id_list': friend_id_list,
           'pending_friend_id_list': pending_friend_id_list,
           'voted_id_list': voted_id_list,
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True, 'querystring': "", 'count': 0, 'user': user })