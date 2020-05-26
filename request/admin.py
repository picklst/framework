from django.contrib import admin
from .models import ListRequest, FollowUserRequest, ListEntry


@admin.register(ListEntry)
class ListEntryAdmin(admin.ModelAdmin):
    pass


@admin.register(FollowUserRequest)
class FollowUserRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(ListRequest)
class ListRequestAdmin(admin.ModelAdmin):
    pass
