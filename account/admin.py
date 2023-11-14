from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo', 'get_photo')
    readonly_fields = ('get_photo',)

    def get_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' height=250 ")
