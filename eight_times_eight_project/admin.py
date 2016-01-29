from django.contrib import admin
from eight_times_eight_project.activities.models import Activity,Notification
from eight_times_eight_project.auth_new.models import Profile,User
from eight_times_eight_project.feeds.models import Feed
from eight_times_eight_project.messages_new.models import Message

admin.site.register(Activity)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Feed)
admin.site.register(Message)