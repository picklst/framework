from django.contrib import admin

from link.models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass

