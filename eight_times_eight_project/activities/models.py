# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape

class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    VOTE = 'V'
    ADD_FRIEND = 'A'
    CONFIRM_FRIEND = 'C'
    DECLINE_FRIEND = 'D'
    PROFILE_VIEW = 'P'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (VOTE, 'Vote'),
        (ADD_FRIEND, 'Add Friend'),
        (CONFIRM_FRIEND, 'Confirm Friend Request'),
        (DECLINE_FRIEND, 'Decline Friend Request'),
        (PROFILE_VIEW, 'View User Profile'),
        )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)

    to_user = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        return self.activity_type

#    def save(self, *args, **kwargs):
#        super(Activity, self).save(*args, **kwargs)
#        if self.activity_type == Activity.FAVORITE:
#            Question = models.get_model('questions', 'Question')
#            question = Question.objects.get(pk=self.question)
#            user = question.user
#            user.profile.reputation = user.profile.reputation + 5
#            user.save()

class Notification(models.Model):
    FAVORITED = 'F'
    LIKED = 'L'
    VOTED = 'V'
    # COMMENTED = 'C'
    ADDED_FRIEND = 'A'
    CONFIRMED_FRIEND = 'C'
    DECLINED_FRIEND = 'D'
    PROFILE_VIEWED = 'P'
    NOTICE = 'N'
    NOTIFICATION_TYPES = (
        (FAVORITED, 'Favorite'),
        (LIKED, 'Liked'),
        (VOTED, 'Voted'),
        # (COMMENTED, 'Commented'),
        (ADDED_FRIEND, 'Add Friend'),
        (CONFIRMED_FRIEND, 'Confirm Friend Request'),
        (DECLINED_FRIEND, 'Decline Friend Request'),
        (PROFILE_VIEWED, 'Viewed user profile'),
        (NOTICE, 'A system notice'),
        )

    _LIKED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> 点赞了: <a href="/feeds/{2}/">{3}</a>'
    _VOTED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> 推荐了你!'
    _ADDED_FRIEND_TEMPLATE = u'<a href="/user/{0}/">{1}</a> 请求添加你为好友！'
    _CONFIRMED_FRIEND_TEMPLATE = u'<a href="/user/{0}/">{1}</a> 和你成为了好友！'
    _DECLINED_FRIEND_TEMPLATE = u'<a href="/user/{0}/">{1}</a> 拒绝了你的好友申请。'
    _PROFILEED_VIEWED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> 查看了你的名片！'
    _NOTICE_TEMPLATE = u'{0}'
    # _COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> 评论了: <a href="/feeds/{2}/">{3}</a>'

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feeds.Feed', null=True, blank=True)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __unicode__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.pk),
                escape(self.from_user.profile.realname),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        # elif self.notification_type == self.COMMENTED:
        #     return self._COMMENTED_TEMPLATE.format(
        #         escape(self.from_user.username),
        #         escape(self.from_user.profile.get_screen_name()),
        #         self.feed.pk,
        #         escape(self.get_summary(self.feed.post))
        #         )
        elif self.notification_type == self.FAVORITED:
            return self._FAVORITED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
                )
        elif self.notification_type == self.VOTED:
            return self._VOTED_TEMPLATE.format(
                escape(self.from_user.pk),
                escape(self.from_user.profile.realname),
                )
        elif self.notification_type == self.ADDED_FRIEND:
            return self._ADDED_FRIEND_TEMPLATE.format(
                escape(self.from_user.pk),
                escape(self.from_user.profile.realname),
                )
        elif self.notification_type == self.CONFIRMED_FRIEND:
            return self._CONFIRMED_FRIEND_TEMPLATE.format(
                escape(self.from_user.pk),
                escape(self.from_user.profile.realname),
                )
        elif self.notification_type == self.DECLINED_FRIEND:
            return self._DECLINED_FRIEND_TEMPLATE.format(
                escape(self.from_user.pk),
                escape(self.from_user.profile.realname),
                )
        elif self.notification_type == self.PROFILE_VIEWED:
            return self._PROFILE_VIEWED_TEMPLATE.format(
                escape(self.from_user.pk),
                escape(self.from_user.profile.realname),
                )
        elif self.notification_type == self.NOTICE:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.get_summary(self.feed.post))
                )
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value