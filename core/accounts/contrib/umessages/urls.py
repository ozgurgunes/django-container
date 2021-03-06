from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from core.accounts.contrib.umessages import views as messages_views

urlpatterns = patterns('',
    url(r'^compose/$',
        messages_views.message_compose,
        name='accounts_umessages_compose'),

    url(r'^compose/(?P<recipients>[\+\.\w]+)/$',
        messages_views.message_compose,
        name='accounts_umessages_compose_to'),

    url(r'^reply/(?P<parent_id>[\d]+)/$',
        messages_views.message_compose,
        name='accounts_umessages_reply'),

    url(r'^view/(?P<username>[\.\w]+)/$',
        messages_views.message_detail,
        name='accounts_umessages_detail'),

    url(r'^remove/$',
        messages_views.message_remove,
        name='accounts_umessages_remove'),

    url(r'^unremove/$',
        messages_views.message_remove,
        {'undo': True},
        name='accounts_umessages_unremove'),

    url(r'^$',
        messages_views.message_list,
        name='accounts_umessages_list'),
)
