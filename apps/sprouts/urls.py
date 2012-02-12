from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from apps.sprouts.models import Sprout
from apps.sprouts.forms import BranchForm
from apps.sprouts import views

date_dict = {
    'queryset'      : Sprout.objects.select_related().all(),
    'date_field'    : 'date_created',
    'extra_context'     : {
        'branch_form'   : BranchForm(),
    }
}

urlpatterns = patterns('django.views.generic.date_based',
        
   url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)$', 'object_detail',
        dict(date_dict, month_format='%m', template_name='sprouts/sprout_detail.html'),
        name='sprouts_archive_detail'),
        
   url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})$', 'archive_day',
        dict(date_dict, month_format='%m'),
        name='sprouts_archive_day'),
        
   url(r'^(?P<year>\d{4})/(?P<month>\d{2})$', 'archive_month',
        dict(date_dict, month_format='%m'),
        name='sprouts_archive_month'),
        
   url(r'^(?P<year>\d{4})$', 'archive_year',
        date_dict,
        name='sprouts_archive_year'),
)

urlpatterns += patterns('',
    url(r'^create/sprout$', views.sprout_create, name='sprouts_sprout_create'),    
    url(r'^update/sprout/(?P<id>\d+)$', views.sprout_update, name='sprouts_sprout_update'),
    url(r'^delete/sprout/(?P<id>\d+)$', views.sprout_delete, name='sprouts_sprout_delete'),
    url(r'^sort/leaves/(?P<id>\d+)$', views.leaf_sort, name='sprouts_leaf_sort'),    
    url(r'^create/leaf/(?P<id>\d+)/(?P<module>[-\w]+)$', views.leaf_create, name='sprouts_leaf_create'),    
    url(r'^create/branch$', views.branch_create, name='sprouts_branch_create'),    
    
    url(r'^tags/$', direct_to_template, {'template': 'sprouts/sprout_tags.html'}, name='sprouts_sprout_tags'),
    url(r'^tags/(?P<tag>.*)/$', views.sprout_tagged, None, name='sprouts_sprout_tagged'),
    url(r'^search/$', views.sprout_search, None, name='sprouts_sprout_search'),
    url(r'^$', views.sprouts_homepage,     None, name='sprouts_homepage'),
)
