from django.contrib import admin
from apps.sprouts.models import *

class BranchInline(admin.StackedInline):
    model                   =   Branch
    fk_name                 =   'source'

class LeafInline(admin.StackedInline):
    model                   =   Leaf

class SproutAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display    = ('title', 'user', 'date_created', 'is_public')
    list_filter     = ['date_created', 'is_public']
    search_fields   = ['title', 'description']
    date_hierarchy  = 'date_created'
    inlines         = [LeafInline, BranchInline]

class BranchAdmin(admin.ModelAdmin):
    list_display    = ('source', 'target', 'user', 'date_created')
        
class LeafAdmin(admin.ModelAdmin):
    list_display    = ('sprout', 'user', 'content_type')
    sortable_field_name = 'position'

admin.site.register(Sprout, SproutAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Leaf, LeafAdmin)
