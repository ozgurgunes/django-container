from django.contrib.contenttypes.models import ContentType
from django.contrib import comments
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from tagging.models import Tag, TaggedItem
from apps.sprouts.models import *
from apps.sprouts.forms import SproutForm, BranchForm
from core.decorators import owner_or_perm_required
from relationships.utils import positive_filter
from django.http import HttpResponse, HttpResponseBadRequest
   
# Create your views here.

@login_required
def sprouts_homepage(request, **kwargs):
    """
    Lists users and followings sprouts
    """
    user_list = User.objects.filter(username=request.user) | request.user.relationships.following()
    queryset = positive_filter(Sprout.objects.select_related().all(), user_list)
    extra_context={'form': SproutForm(initial={'user': request.user})}
    return object_list(request, queryset=queryset, template_name='sprouts/home_sprouts.html', extra_context=extra_context)


@login_required
def sprout_create(request):
    extra_context={'form': SproutForm(initial={'user': request.user})}
    if request.method == 'POST':
        form = SproutForm(request.POST)
        if form.is_valid():
            # TODO: Need serious improvements and refactoring below
            sprout = form.save()            
            extra_context['created'] = True
            extra_context['object'] = sprout 
            return redirect(sprout)
        else:
            extra_context = {'form': SproutForm(request.POST)}
    extra_context['user'] = request.user
    return render_to_response('sprouts/sprout_create.html', extra_context, context_instance=RequestContext(request))

@owner_or_perm_required(Sprout, 'sprouts.can_change')
def sprout_update(request, id=None):
    sprout = get_object_or_404(Sprout, pk=id)
    if request.method == 'POST':
        form = SproutForm(request.POST, request.FILES, instance=sprout)
        if form.is_valid():
            sprout = form.save()
            return redirect(sprout)
            #return render_to_response('sprouts/sprout_update.html', {'updated': True, 'form': form, 'user': request.user, 'object': sprout}, context_instance=RequestContext(request))
    else:
        errors = data = {}
        form = SproutForm(instance=sprout)
    return render_to_response('sprouts/sprout_update.html', {'form': form, 'user': request.user, 'object': sprout}, context_instance=RequestContext(request))

@owner_or_perm_required(Sprout, 'sprouts.can_delete')
def sprout_delete(request, id=None):
    sprout = get_object_or_404(Sprout, pk=id)
    p = str(sprout)
    comments.get_model().objects.filter(content_type__pk=ContentType.objects.get_for_model(Sprout).id, object_pk=sprout.id).delete()
    sprout.delete()
    return redirect('sprouts_sprout_list')
    
@owner_or_perm_required(Branch, 'sprouts.can_change')
def branch_create(request):
    extra_context={'form': BranchForm(initial={'user': request.user})}
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save()            
            extra_context['created'] = True
            extra_context['object'] = branch 
            return redirect(branch.source)
        else:
            extra_context = {'form': BranchForm(request.POST)}
    return render_to_response('sprouts/branch_create.html', extra_context, context_instance=RequestContext(request))
    
@owner_or_perm_required(Branch, 'sprouts.can_delete')
def branch_delete(request, leaf_id=None):
    pass

@owner_or_perm_required(Sprout, 'sprouts.can_change')
def leaf_create(request, id=None, module=None):
    sprout = get_object_or_404(Sprout, pk=id)
    extra_context = { 'module': module, 'sprout': sprout }
    return render_to_response('sprouts/leaf_create_ajax.html', extra_context, context_instance=RequestContext(request))

@owner_or_perm_required(Sprout, 'sprouts.can_delete')
def leaf_sort(request, id=None):
    sprout = get_object_or_404(Sprout, pk=id)
    if request.method == 'POST':
        for position, pk in enumerate(request.POST.getlist('leaf[]')):
            Leaf.objects.filter(pk=pk).update(position=position+1)
    extra_context = { 'object': sprout }
    return render_to_response('sprouts/_sprout_leaves.html', extra_context, context_instance=RequestContext(request))
        

def sprout_tagged(request, tag, template_name='sprouts/sprout_tagged.html', **kwargs):
    tag                 = tag.replace('-',' ')
    query_tag           = Tag.objects.get(name=tag)
    kwargs['queryset']  = TaggedItem.objects.get_by_model(Sprout, query_tag).order_by('-date_created')
    kwargs['extra_context'] = {
        'tag'       : tag,
        'user'      : request.user,
    }
    return object_list(request, template_name=template_name, **kwargs)

def sprout_search(request, template_name='sprouts/sprout_search.html', **kwargs):
    keyword     = request.GET.get('s', '')
    kwargs['queryset'] = Sprout.objects.search(keyword)
    kwargs['extra_context'] = {
        'keyword'   : keyword,
        'user'      : request.user,
    }
    return object_list(request, template_name=template_name, **kwargs)
