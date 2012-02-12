from django.contrib import admin
from apps.atlas.models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)

class SpodAdmin(admin.ModelAdmin):
    list_display  = ('title', 'latitude', 'longitude', 'created')
    list_filter   = ('title', 'created')
    search_fields = ('title', 'spotline', 'latitude', 'longitude')
    #prepopulated_fields = {'slug': ('title',)}

admin.site.register(Spod, SpodAdmin)