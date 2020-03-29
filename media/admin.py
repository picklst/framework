from django.contrib import admin
from media.models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass