import graphene

from list.models import ItemMedia
from log.models import ItemChangeLog
from media.api.objects import MediaObj


class ItemObj(graphene.ObjectType):
    name = graphene.String()
    key = graphene.String()
    comment = graphene.String()
    url = graphene.String()
    media = graphene.Field(MediaObj)
    nextItem = graphene.Field(lambda: ItemObj)
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


class PositionResolvedItemObj(ItemObj):
    position = graphene.Int()

    def resolve_createdTimestamp(self, info):
        log = ItemChangeLog.objects.filter(item=self['item']).order_by('timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_lastUpdateTimestamp(self, info):
        log = ItemChangeLog.objects.filter(item=self['item']).order_by('-timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_media(self, info):
        try:
            return ItemMedia.objects.get(item=self['item']).media
        except ItemMedia.DoesNotExist:
            return None

    def resolve_name(self, info):
        return self['item'].name

    def resolve_key(self, info):
        return self['item'].key

    def resolve_comment(self, info):
        return self['item'].comment

    def resolve_url(self, info):
        return self['item'].url

    def resolve_nextItem(self, info):
        return self['nextItem']

    def resolve_position(self, info):
        return self['position']
