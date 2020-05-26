from django.contrib import admin

from curation.models import FeaturedList


@admin.register(FeaturedList)
class FeaturedListAdmin(admin.ModelAdmin):
    pass
