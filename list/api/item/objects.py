import graphene

from log.models import ItemChangeLog


class ItemObj(graphene.ObjectType):
    name = graphene.String()
    key = graphene.String()
    comment = graphene.String()
    url = graphene.String()
    nextItem = graphene.Field(lambda: ItemObj)
    createdTimestamp = graphene.types.DateTime()
    lastUpdateTimestamp = graphene.types.DateTime()

    def resolve_createdTimestamp(self, info):
        log = ItemChangeLog.objects.filter(list=self).order_by('timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_lastUpdateTimestamp(self, info):
        log = ItemChangeLog.objects.filter(list=self).order_by('-timestamp')
        if log.first():
            return log.first().timestamp


class PositionResolvedItemObj(ItemObj):
    position = graphene.Int()

    def resolve_createdTimestamp(self, info):
        log = ItemChangeLog.objects.filter(list=self['item']).order_by('timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_lastUpdateTimestamp(self, info):
        log = ItemChangeLog.objects.filter(list=self['item']).order_by('-timestamp')
        if log.first():
            return log.first().timestamp

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
