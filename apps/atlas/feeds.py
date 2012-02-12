from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from basic.atlas.models import Spod, Category


class AtlasSpodsFeed(Feed):
    title_template = 'feeds/spods_title.html'
    description_template = 'feeds/spods_description.html'

    _site = Site.objects.get_current()
    title = '%s Atlas' % _site.name
    description = '%s spods feed.' % _site.name

    def link(self):
        return reverse('atlas_index')

    def items(self):
        return Spod.objects.published()[:10]

    def item_pubdate(self, obj):
        return obj.publish


class AtlasSpodsByCategory(Feed):
    title_template = 'feeds/spods_title.html'
    description_template = 'feeds/spods_description.html'
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits[0])

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def title(self, obj):
        return "%s Atlas - %s feed" % (Site.objects.get_current().name, obj.title)

    def description(self, obj):
        return "Spods recently categorized as %s" % obj.title
    
    def items(self, obj):
        return obj.spod_set.published()[:10]Atlas