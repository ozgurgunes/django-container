from django.shortcuts import render_to_response, get_object_or_404
from apps.bannerstore.models import *
from django.template import RequestContext

def client_detail(request,clientName,token):
	client = Client.objects.get(slug=clientName)
	campaigns= client.campaign_set.all()
	extra_context = {
        'client': client,
	    'campaigns': campaigns,
        }
	if client.token==token:
		return render_to_response('bannerstore/client_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')
	
def campaign_detail(request,clientName,campaignName,token):
	campaign = Campaign.objects.get(slug=campaignName)
	banners = campaign.banner_set.all()
	extra_context = {
        'campaign': campaign,
	    'banners': banners
        }
	if campaign.token==token:
		return render_to_response('bannerstore/campaign_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')

def banner_detail(request,clientName,campaignName,id,token):
	banner=Banner.objects.all().get(id=id)
	versions=banner.version_set.all().order_by('-revision')
	version = versions[0]
	extra_context = {
        'banner': banner,
        'versions': versions,
        'version': version
        }
	if banner.token==token:
		return render_to_response('bannerstore/show_banner_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')

def banner_version(request,clientName,campaignName,id,token,revNo):
	banner=Banner.objects.all().get(id=id)
	versions=banner.version_set.all().order_by('-revision')
	version=versions.get(revision=revNo)
	extra_context = {
        'banner': banner,
        'versions': versions,
	    'version': version
        }
	if banner.token==token:
		return render_to_response('bannerstore/show_banner_detail.html',extra_context,context_instance=RequestContext(request))
	else:
		return render_to_response('error.html')
	
   
	
