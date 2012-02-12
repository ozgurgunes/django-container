from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from apps.atlas import managers

def image_upload_to(instance, filename):
    return 'uploads/pictures/spods/%s_%s' % (str(instance.id), filename)

class Category(models.Model):
    """Category model."""
    title       = models.CharField(_('title'), max_length=100)
    slug        = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'))
    image       = models.ImageField(upload_to=image_upload_to, blank=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'atlas_categories'
        ordering = ('title',)

    class Admin:
        pass

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('atlas_category_detail', None, {'slug': self.slug})

class Spod(models.Model):

    STATUS_CHOICES = (
        (-1, _('Flaged')),
        (0, _('Deleted')),
        (1, _('Draft')),
        (2, _('Public')),
    )

    user            = models.ForeignKey(User, blank=True, null=True)
    title           = models.CharField(_('title'), max_length=155)
    spotline        = models.TextField(_('spotline'), blank=True)
    image           = models.ImageField(upload_to=image_upload_to, blank=True)
    
    latitude        = models.FloatField(_('latitude'))
    longitude       = models.FloatField(_('longitude'))

    created         = models.DateTimeField(_('created'), auto_now_add=True)
    modified        = models.DateTimeField(_('modified'), auto_now=True)
    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    
    imdb_url        = models.URLField(null=True, blank=True)
    tube_url        = models.URLField(null=True, blank=True)
    
    objects         = managers.SpodManager()
    
    class Meta:
        verbose_name = _('spod')
        verbose_name_plural = _('atlas')
        db_table  = 'atlas_spod'
        ordering  = ('title',)
        get_latest_by = 'created'

    class Admin:
        pass
        
    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('spod_detail', None, {'object_id': str(self.id)})

class Favorite(models.Model):
    """
    Favorite nodes
    
    """
    
    spod                    = models.ForeignKey(Spod)
    user                    = models.ForeignKey(User)
    date_created            = models.DateTimeField(_('date created'), auto_now_add=True)
    
    objects                 = managers.FavoriteManager()

