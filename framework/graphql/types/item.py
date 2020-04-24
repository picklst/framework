import graphene

from list.models import ItemMedia
from log.models import ItemChangeLog


class Item(graphene.ObjectType):
    from .media import Media as MediaObj

    name = graphene.String()
    key = graphene.String()
    comment = graphene.String()
    url = graphene.String()
    media = graphene.Field(MediaObj)
    nextItem = graphene.Field(lambda: Item)
    createdTimestamp = graphene.types.DateTime()
    lastUpdateTimestamp = graphene.types.DateTime()

    def resolve_createdTimestamp(self, info):
        log = ItemChangeLog.objects.filter(item=self).order_by('timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_lastUpdateTimestamp(self, info):
        log = ItemChangeLog.objects.filter(item=self).order_by('-timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_media(self, info):
        try:
            return ItemMedia.objects.get(item=self)
        except ItemMedia.DoesNotExist:
            return None
