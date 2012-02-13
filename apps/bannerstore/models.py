import re
from datetime import datetime
from hashlib import md5
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters

def get_upload_to_version(instance, filename):
    return 'uploads/banners/%s_%s' % (str(instance.revision), re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))

def get_upload_to_client(instance, filename):
   	return 'uploads/clients/%s_%s' % (str(instance.id), re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))

def get_upload_to_mediaplan(instance, filename):
   	return 'uploads/campaigns/%s_%s' % (str(instance.id), re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))

def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), str(instance._meta.module_name), re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))


class Client(models.Model):
	title           = models.CharField(_(u'title'), max_length=100, unique=True)
	slug            = models.CharField(_(u'slug'), max_length=100)
	about           = models.TextField(_(u'about'), blank=True)
	website         = models.CharField(_(u'website'), max_length=150)
	logo            = models.ImageField(_(u'logo'), upload_to=get_upload_to, blank=True)
	token           = models.CharField(_(u'token'), max_length=32, blank=True)
	created_at      = models.DateTimeField(_(u'created at'), auto_now_add=True)
	
	
	def __unicode__(self):
		return u'%s' % self.title

	@models.permalink
	def get_absolute_url(self):
		return ('client_detail',(), {
		    'clientName': self.slug,
   	        'token': self.token
   	    })

	def save(self):
		if not self.slug:
			self.slug=defaultfilters.slugify(self.title)
   		if not self.token:
			hash_str = md5(str(datetime.now())).hexdigest()
   			self.token = hash_str
   		super(Client, self).save()
		
class Campaign(models.Model):
	client           = models.ForeignKey(Client, blank=False, null=False)
	title            = models.CharField(_(u'title'), max_length=100)
	slug             = models.CharField(_(u'slug'), max_length=100)
	summary          = models.TextField(_(u'summary'), blank=True)
	mediaplan        = models.FileField(_(u'mediaplan'), upload_to=get_upload_to, blank=True)
	token            = models.CharField(_(u'token'), max_length=32)
	created_at       = models.DateTimeField(_(u'created at'), auto_now_add=True)
	
	
	def __unicode__(self):
		return u'%s' % self.title

	@models.permalink
	def get_absolute_url(self):
		return ('campaign_detail',(), {
		    'clientName': self.client.slug,
		    'campaignName': self.slug,
   	        'token': self.token
   	    })

	def save(self):
		if not self.slug:
			self.slug=defaultfilters.slugify(self.title)
   		if not self.token:
			hash_str = md5(str(datetime.now())).hexdigest()
   			self.token = hash_str
   		super(Campaign, self).save()
		
class Size(models.Model):
    """size model"""
    ATTRIBUTE_CHOICES = (
        (1, _(u'Normal')),
        (2, _(u'Floating')),
        (3, _(u'Pageskin')),
        (4, _(u'Rich')),
        (5, _(u'Widget')),
    )
    
    width           = models.IntegerField(_(u'width'), default=0, blank=False, null=False)
    height          = models.IntegerField(_(u'height'), default=0, blank=False, null=False)
    attribute       = models.IntegerField(_(u'attribute'), choices=ATTRIBUTE_CHOICES, default=1)	

    def __unicode__(self):
        return u'%s x %s (%s)' % (self.width, self.height, self.get_attribute_display())
		
class Banner(models.Model):
	campaign           = models.ForeignKey(Campaign, blank=False, null=False)
	size           	   = models.ForeignKey(Size, blank=False, null=False)
	description        = models.TextField(_(u'description'), blank=True)
	token              = models.CharField(_(u'token'), max_length=200)
	created_at         = models.DateTimeField(_(u'created at'), auto_now_add=True)
	
	
	def __unicode__(self):
		return u'%s' % self.size
		
	@models.permalink
	def get_absolute_url(self):
		return ('banner_detail',(), {
		    'clientName': self.campaign.client.slug,
		    'campaignName': self.campaign.slug,
   	        'id': self.id,
   	        'token': self.token
   	    })
   	    
   	def client(self):
   	    return self.campaign.client
   
   	def save(self):
   		if not self.token:
			hash_str = md5(str(datetime.now())).hexdigest()
   			self.token = hash_str
   		super(Banner, self).save()
   		
class Version(models.Model):
	banner           = models.ForeignKey(Banner, blank=False, null=False)
	revision         = models.IntegerField(_(u'revision'), blank=True, null=False)
	comment          = models.TextField(_(u'comment'), blank=True)
	file             = models.FileField(_(u'file'), upload_to=get_upload_to, blank=False)
	alternative      = models.ImageField(_(u'alternative'), upload_to=get_upload_to, blank=True)
	created_at       = models.DateTimeField(_(u'created at'), auto_now_add=True)
	
	
	def __unicode__(self):
		return u'Revizyon: %s' % self.revision

	@models.permalink
	def get_absolute_url(self):
		return ('banner_version',(), {
		    'clientName': self.banner.client().slug,
		    'campaignName': self.banner.campaign.slug,
   	        'id': self.banner.id,
   	        'token': self.banner.token,
   	        'revNo': self.revision
   	    })

	def save(self):
   		if not self.revision:
			versions=self.banner.version_set.order_by('-revision')
			if not versions:
				self.revision=1
			else:
				self.revision=versions[0].revision+1	
   		super(Version, self).save()
		
