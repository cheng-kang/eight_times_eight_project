from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'eight_times_eight_project.core.views.home', name='home'),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'core/cover.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', 'eight_times_eight_project.auth_new.views.signup', name='signup'),
    url(r'^settings/$', 'eight_times_eight_project.core.views.settings', name='settings'),
    url(r'^settings/picture/$', 'eight_times_eight_project.core.views.picture', name='picture'),
    url(r'^settings/upload_picture/$', 'eight_times_eight_project.core.views.upload_picture', name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', 'eight_times_eight_project.core.views.save_uploaded_picture', name='save_uploaded_picture'),
    url(r'^settings/password/$', 'eight_times_eight_project.core.views.password', name='password'),
    url(r'^network/$', 'eight_times_eight_project.core.views.network', name='network'),
    url(r'^feeds/', include('eight_times_eight_project.feeds.urls')),
    url(r'^messages/', include('eight_times_eight_project.messages_new.urls')),
    url(r'^notifications/$', 'eight_times_eight_project.activities.views.notifications', name='notifications'),
    url(r'^notifications/last/$', 'eight_times_eight_project.activities.views.last_notifications', name='last_notifications'),
    url(r'^notifications/check/$', 'eight_times_eight_project.activities.views.check_notifications', name='check_notifications'),
    url(r'^search/$', 'eight_times_eight_project.search.views.search', name='search'),
    url(r'^(?P<username>[^/]+)/$', 'eight_times_eight_project.core.views.profile', name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
