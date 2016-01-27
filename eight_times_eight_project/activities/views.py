from django.shortcuts import render
from eight_times_eight_project.activities.models import Notification
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from eight_times_eight_project.decorators import ajax_required

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user).exclude(notification_type='A')
    add_friend_notifications = Notification.objects.filter(to_user=user, notification_type='A')
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()
    count = add_friend_notifications.count()
    return render(request, 'activities/notifications.html', {'count': count, 'notifications': notifications, 'add_friend_notifications': add_friend_notifications})

@login_required
@ajax_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'activities/last_notifications.html', {'notifications': notifications})

@login_required
@ajax_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    return HttpResponse(len(notifications))