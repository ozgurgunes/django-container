from django.conf.urls.defaults import *
from core.profiles import views, forms
from relationships import views as relationship_views

urlpatterns = patterns('',

    url(r'settings/$',
        views.profile_settings, dict(template_name='profiles/profile_settings.html'), name='profiles_profile_settings'),
    url(r'^edit/$',
        views.profile_edit, dict(form=forms.ProfileForm), name='profiles_edit_profile'),
    url(r'^edit/mugshot/$',
        views.mugshot_upload, dict(form=forms.MugshotForm), name='profiles_edit_mugshot'),
    url(r'^edit/name/$',
        views.user_edit, dict(form=forms.NameForm), name='profiles_edit_name'),
    url(r'^edit/email/$',
        views.user_edit, dict(form=forms.EmailForm), name='profiles_edit_email'),
    url(r'^edit/services/$',
        views.profile_edit, dict(form=forms.ServiceFormSet, template_name='profiles/profile_formset_services.html'), name='profiles_edit_services'),
    url(r'^edit/links/$',
        views.profile_edit, dict(form=forms.LinkFormSet, template_name='profiles/profile_formset_links.html'), name='profiles_edit_links'),    


    url(r'^(?P<username>\w+)/$', views.profile_detail, name='profiles_profile_detail'),
    url(r'^(?P<username>\w+)/comments/$', views.comment_list, name='profiles_comment_list'),

    url(r'^(?P<username>\w+)/friends/$', views.friend_list, name='profiles_friend_list'),

    url(r'^$', views.profile_list, name='profiles_profile_list'),
    
)
