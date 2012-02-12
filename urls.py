from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'homepage.html',}, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('core.accounts.urls')),
    url(r'^profiles/', include('core.profiles.urls')),
    url(r'^notices/', include('notification.urls')),
    url(r'^announcements/', include('announcements.urls')),
#    url(r'^about/', include('about.urls')),
)
