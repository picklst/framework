from django.contrib import admin
from taxonomy.models import Topic, Tag


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


