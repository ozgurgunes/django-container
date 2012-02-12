from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from tagging.models import Tag
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from core.models import SlugifyUniquely

class Sprout(models.Model):
    """
    Topic class for Sprouts application
    """
    user                    = models.ForeignKey(User)
    title                   = models.CharField(max_length=216)
    slug                    = models.SlugField(max_length=216, blank=True, null=False)
    date_created            = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    is_public               = models.BooleanField(default=True)

    branches                = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, through='Branch', related_name='trunks')

    tags                    = TagField()
    
    class Meta:
        ordering                = ('-date_created', 'title')
        verbose_name            = _('Sprout')
        verbose_name_plural     = _('Sprouts')
        get_latest_by           = 'date_created'

    def __unicode__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        # Populate slug field
        if not self.id:
            self.slug   = str(SlugifyUniquely(self.title, self.__class__)) #str(slugify(self.title))
        super(Sprout, self).save(*args, **kwargs) 
        
    def delete(self):
        super(Sprout, self).delete()

    @models.permalink
    def get_absolute_url(self):
        return ('sprouts_archive_detail', None, {
            'year': self.date_created.year,
            'month': self.date_created.strftime('%m'),
            'day': self.date_created.day,
            'slug': self.slug
            })

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tags):
        Tag.objects.update_tags(self, tag_list)

    tag_list = property(_get_tags, _set_tags)

    
class Branch(models.Model):
    """
    Component class for Sprout object
    """
    source              = models.ForeignKey(Sprout, related_name='branch_set')
    target              = models.ForeignKey(Sprout, related_name='trunk_set')
    
    user                    = models.ForeignKey(User)
    date_created            = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    
    class Meta:
        unique_together = (('source', 'target'),)
        ordering                = ('-date_created',)
        verbose_name            = _('Branch')
        verbose_name_plural     = _('Branches')
        get_latest_by           = 'date_created'

    def __unicode__(self):
        return u"%s > %s" % (self.source, self.target)

class Leaf(models.Model):
    """
    Extension class for Sprout object
    """
    content_type            = models.ForeignKey(ContentType)
    object_id               = models.PositiveIntegerField()
    content_object          = generic.GenericForeignKey()
        

    user                    = models.ForeignKey(User)
    sprout                  = models.ForeignKey(Sprout)
    date_created            = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    
    position                = models.PositiveSmallIntegerField(blank=True, null=False, default=0, editable=False);
    
    class Meta:
        ordering                = ('position', '-date_created',)
        verbose_name            = _('Leaf')
        verbose_name_plural     = _('Leaves')
        get_latest_by           = 'date_created'

    def __unicode__(self):
        return u"%s" % self.content_object
        
    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.position = Leaf.objects.filter(sprout=self.sprout).aggregate(models.Max('position'))['position__max'] + 1
            except:
                self.position = 1
        super(Leaf, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('leaf_detail', None, {
            'leaf_pk': self.pk,
            })

    def list_template(self):
        try:
            return self.content_object.leaf_template('list')
        except AttributeError:
            return u"%s/_%s_leaf_list.html" % (self.content_type.app_label, self.content_type.name.lower())

    def detail_template(self):
        try:
            return self.content_object.leaf_template('detail')
        except AttributeError:
            return u"%s/_%s_leaf_detail.html" % (self.content_type.app_label, self.content_type.name.lower())

class LeafBase(models.Model):
    """Abstract base class for leaf contents"""

    user            = models.ForeignKey(User, blank=False, null=False)
    sprout          = models.ForeignKey(Sprout, blank=False, null=False)
    date_created    = models.DateTimeField(blank=True, null=False, auto_now_add=True)

    class Meta:
        abstract        = True
        ordering        = ('-date_created',)
        get_latest_by   = 'date_created'

    def leaf_template(self, template=None):
        if template == 'list':
            return u"%s/_%s_leaf_list.html" % (self._meta.app_label, self._meta.module_name.lower())
        elif template == 'detail':
            return u"%s/_%s_leaf_detail.html" % (self._meta.app_label, self._meta.module_name.lower())
        else:    
            return u"%s/_%s_leaf.html" % (self._meta.app_label, self._meta.module_name.lower())
