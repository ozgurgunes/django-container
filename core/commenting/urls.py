from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^delete/(?P<comment_id>\d+)/$', 'apps.commenting.views.delete'),
    (r'', include('django.contrib.comments.urls')),
)