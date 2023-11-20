from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import *

from images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'image', 'created', 'get_image')
    list_filter = ('created',)
    readonly_fields = ('get_image',)

    def get_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' height=100 ")

