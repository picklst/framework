import graphene

from framework.utils.graphql import APIException
from list.models import List
from log.models import ListChangeLog


class ListPropertiesObj(graphene.ObjectType):
    isPrivate = graphene.Boolean()
    isRanked = graphene.Boolean()
    forceCuratorRanking = graphene.Boolean()
    isVotable = graphene.Boolean()
    areVotesPrivate = graphene.Boolean()
    canVoteMultipleItems = graphene.Boolean()
    isRateable = graphene.Boolean()
    areRatingsPrivate = graphene.Boolean()
    acceptEntries = graphene.Boolean()


class ListObj(graphene.ObjectType):
    from taxonomy.api.tag.objects import TagObj
    from user.api.user.objects import UserObj
    from list.api.item.objects import PositionResolvedItemObj

    name = graphene.String()
    slug = graphene.String()
    curator = graphene.Field(UserObj)
    createdTimestamp = graphene.types.DateTime()
    lastUpdateTimestamp = graphene.types.DateTime()

    coverURL = graphene.String()
    description = graphene.String()
    properties = graphene.Field(ListPropertiesObj)

    tags = graphene.List(TagObj)
    items = graphene.List(PositionResolvedItemObj)
    itemCount = graphene.Int()

    def resolve_coverURL(self, info):
        if self.cover and hasattr(self.cover, 'url'):
            return info.context.build_absolute_uri(self.cover.url)
        return None

    def resolve_properties(self, info):
        return self

    def resolve_createdTimestamp(self, info):
        log = ListChangeLog.objects.filter(list=self).order_by('timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_lastUpdateTimestamp(self, info):
        log = ListChangeLog.objects.filter(list=self).order_by('-timestamp')
        if log.first():
            return log.first().timestamp

    def resolve_items(self, info):
        from list.models import Position
        try:
            items = []
            counter = 0
            ItemPos = None
            while ItemPos is None or ItemPos.next is not None:
                if ItemPos is None:
                    listObj = List.objects.get(slug=self.slug)
                    ItemPos = Position.objects.get(list=self, item=listObj.firstItem)
                else:
                    ItemPos = Position.objects.get(list=self, item=ItemPos.next)
                counter += 1
                items.append({
                    "position": counter,
                    "item": ItemPos.item,
                    "nextItem": ItemPos.next,
                })
            return items
        except Position.DoesNotExist:
            raise APIException('List item positions cannot be determined.', code='POSITION_CORRUPTED')

    def resolve_itemCount(self, info):
        return len(self.items.all())
