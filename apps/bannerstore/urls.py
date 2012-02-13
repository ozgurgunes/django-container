from django.conf.urls.defaults import *
from apps.bannerstore import views as bannerstore_views

urlpatterns = patterns('',

    url(r'^(?P<clientName>[-\w]+)/(?P<campaignName>[-\w]+)/(?P<id>\d+)/(?P<token>[-\w]+)/(?P<revNo>[-\d]+)/',
        bannerstore_views.banner_version, name='banner_version'),

    url(r'^(?P<clientName>[-\w]+)/(?P<campaignName>[-\w]+)/(?P<id>\d+)/(?P<token>[-\w]+)/',
        bannerstore_views.banner_detail, name='banner_detail'),

    url(r'^(?P<clientName>[-\w]+)/(?P<campaignName>[-\w]+)/(?P<token>[-\w]+)/',
        bannerstore_views.campaign_detail, name='campaign_detail'),

    url(r'^(?P<clientName>[-\w]+)/(?P<token>[-\w]+)/',
        bannerstore_views.client_detail, name='client_detail'),

)