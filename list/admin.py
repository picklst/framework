from django.contrib import admin
from list.models import List, Collaborator, Item, Position, Vote, Rating


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    pass


@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class PositionAdmin(admin.ModelAdmin):
    pass
