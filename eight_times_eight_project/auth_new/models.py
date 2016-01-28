# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings
import os.path
from eight_times_eight_project.activities.models import Notification
import urllib, hashlib

class Profile(models.Model):

    GENDERS = (
        ('m', "男"),
        ('f', "女"),
    )

    ACCOUNT_STATUS = (
        ('n', '正常'),
        ('b', '禁用'),
        ('s', '停用'),
    )

    user = models.OneToOneField(User)
    realname = models.CharField('真实姓名', max_length=50)
    major = models.CharField('专业', max_length=50)
    enter_year = models.CharField('入学年份', max_length=4)
    wechat = models.CharField('微信', max_length=50, blank=True, default="")
    phone = models.CharField('手机号', max_length=50, blank=True, default="")
    address = models.CharField('地址', max_length=50, blank=True, default="")

    gender = models.CharField('性别', max_length=1, choices=GENDERS, default=GENDERS[0][0], blank=True)

    friends = models.IntegerField('好友数', default=0, blank=True)
    views = models.IntegerField('浏览量', default=0, blank=True)
    votes = models.IntegerField('推荐数', default=0, blank=True)

    v_email = models.SmallIntegerField("邮箱验证", default=0, blank=True)
    v_tel = models.SmallIntegerField("手机验证", default=0, blank=True)
    v_edu = models.SmallIntegerField("校友身份验证", default=0, blank=True)

    status = models.CharField('账号状态', max_length=1, choices=ACCOUNT_STATUS, default=ACCOUNT_STATUS[0][0], blank=True)


    personal_website = models.CharField('个人主页', max_length=50, null=True, blank=True, default="")

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url 

    def get_picture(self):
        no_picture = settings.STATIC_URL + 'img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                return no_picture
        except Exception, e:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                from_user=self.user,
                to_user=feed.user,
                feed=feed).save()

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                from_user=self.user, 
                to_user=feed.user, 
                feed=feed).delete()

    def notify_voted(self, user):
        if self.user != user:
            Notification(notification_type=Notification.VOTED,
                from_user=self.user,
                to_user=user,
                         ).save()

    def unotify_voted(self, user):
        if self.user != user:
            Notification.objects.filter(notification_type=Notification.VOTED,
                from_user=self.user,
                to_user=user,
                ).delete()

    def notify_added(self, user):
        if self.user != user:
            Notification(notification_type=Notification.ADDED_FRIEND,
                from_user=self.user,
                to_user=user,
                         ).save()

    def unotify_added(self, user):
        if self.user != user:
            Notification.objects.filter(notification_type=Notification.ADDED_FRIEND,
                from_user=self.user,
                to_user=user,
                ).delete()

    def notify_confirmed(self, user):
        if self.user != user:
            Notification(notification_type=Notification.CONFIRMED_FRIEND,
                from_user=self.user,
                to_user=user,
                         ).save()

    def unotify_confirmed(self, user):
        if self.user != user:
            Notification.objects.filter(notification_type=Notification.CONFIRMED_FRIEND,
                from_user=self.user,
                to_user=user,
                ).delete()

    def notify_declined(self, user):
        if self.user != user:
            Notification(notification_type=Notification.DECLINED_FRIEND,
                from_user=self.user,
                to_user=user,
                         ).save()

    def unotify_declined(self, user):
        if self.user != user:
            Notification.objects.filter(notification_type=Notification.DECLINED_FRIEND,
                from_user=self.user,
                to_user=user,
                ).delete()

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                        from_user=self.user,
                        to_user=feed.user,
                        feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                from_user=self.user,
                to_user=User(id=user),
                feed=feed).save()

    def notify_favorited(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.FAVORITED,
                from_user=self.user, 
                to_user=question.user, 
                question=question).save()

    def unotify_favorited(self, question):
        if self.user != question.user:
            Notification.objects.filter(notification_type=Notification.FAVORITED,
                from_user=self.user, 
                to_user=question.user, 
                question=question).delete()

    def notify_answered(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                from_user=self.user, 
                to_user=question.user, 
                question=question).save()
    
    def notify_accepted(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user, 
                to_user=answer.user, 
                answer=answer).save()
    
    def unotify_accepted(self, answer):
        if self.user != answer.user:
            Notification.objects.filter(notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user, 
                to_user=answer.user, 
                answer=answer).delete()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)