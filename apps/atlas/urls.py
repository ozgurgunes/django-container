from django.conf.urls.defaults import *
from apps.atlas import views as atlas_views

urlpatterns = patterns('',
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/$',
        view=atlas_views.spod_archive_day,
        name='atlas_archive_day'),

    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$',
        view=atlas_views.spod_archive_month,
        name='atlas_archive_month'),

    url(r'^archive/(?P<year>\d{4})/$',
        view=atlas_views.spod_archive_year,
        name='atlas_archive_year'),

    url(r'^(?P<object_id>\d+)/$',
        view=atlas_views.spod_detail,
        name='spod_detail'),

    url (r'^add/$',
        view=atlas_views.atlas_add,
        name='atlas_add'),

    url (r'^create/$',
        view=atlas_views.spod_create,
        name='spod_create'),

    url(r'^categories/(?P<slug>[-\w]+)/$',
        view=atlas_views.category_detail,
        name='atlas_category_detail'),

    url (r'^categories/$',
        view=atlas_views.category_list,
        name='atlas_category_list'),

    url(r'^tags/$', 'django.views.generic.simple.direct_to_template', {'template': 'atlas/tag_list.html'}, name='atlas_tag_list'),
    url(r'^tags/(?P<tag>.*)/$', atlas_views.tag_detail, dict(paginate_by=15), name='atlas_tag_detail'),

    url (r'^search/$',
        view=atlas_views.search,
        name='atlas_search'),

    url(r'^page/(?P<page>\w)/$',
        view=atlas_views.spod_list,
        name='atlas_index_paginated'),

    url(r'^$',
        view=atlas_views.spod_list,
        name='atlas_index'),

)