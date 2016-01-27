from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from eight_times_eight_project.feeds.models import Feed
from django.contrib.auth.decorators import login_required
from eight_times_eight_project.auth_new.models import Profile

@login_required
def search(request):

    if request.user:
        user = request.user
    else:
        user = None

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
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True, 'querystring': "", 'count': 0, 'user': user })