import graphene

from framework.graphql.utils import APIException
from list.models import List as ListModel, Collaborator, ListVote
from request.models import ListEntry


class ListItem(graphene.ObjectType):
    from .item import Item as ItemObj
    position = graphene.Int()
    id = graphene.String()
    item = graphene.Field(ItemObj)
    nextItem = graphene.String()


class ListProperties(graphene.ObjectType):
    isPrivate = graphene.Boolean()
    isRanked = graphene.Boolean()
    forceCuratorRanking = graphene.Boolean()
    isVotable = graphene.Boolean()
    areVotesPrivate = graphene.Boolean()
    canVoteMultipleItems = graphene.Boolean()
    isRateable = graphene.Boolean()
    areRatingsPrivate = graphene.Boolean()
    acceptEntries = graphene.Boolean()


class List(graphene.ObjectType):
    from .tag import Tag as TagObj
    from .user import Profile
    from .item import Item as ItemObj
    from .topic import Topic as TopicObj
    from .vote import ListVoteStats

    id = graphene.String()
    name = graphene.String()
    previewURL = graphene.String()
    slug = graphene.String()
    description = graphene.String()
    curator = graphene.Field(Profile)
    timestampCreated = graphene.types.DateTime()
    timestampLastEdited = graphene.types.DateTime()

    coverURL = graphene.String()
    properties = graphene.Field(ListProperties)
    topic = graphene.Field(TopicObj)
    tags = graphene.List(TagObj)
    items = graphene.List(ListItem, count=graphene.Int(), starting=graphene.String())
    itemCount = graphene.Int()

    userCanEdit = graphene.Boolean()
    hasEntries = graphene.Boolean()

    votes = graphene.Field(ListVoteStats)
    userVote = graphene.Field(ItemObj)

    def resolve_previewURL(self, info):
        return self.curator.username + '/' + self.slug

    def resolve_coverURL(self, info):
        if self.cover and hasattr(self.cover, 'url'):
            return info.context.build_absolute_uri(self.cover.url)
        return None

    def resolve_properties(self, info):
        return self

    # def resolve_createdTimestamp(self, info):
    #     log = ListChangeLog.objects.filter(list=self).order_by('timestamp')
    #     if log.first():
    #         return log.first().timestamp
    #
    # def resolve_lastUpdateTimestamp(self, info):
    #     log = ListChangeLog.objects.filter(list=self).order_by('-timestamp')
    #     if log.first():
    #         return log.first().timestamp

    def resolve_items(self, info, count=10, starting="-1"):
        from list.models import Position
        try:
            items = []
            counter = 0
            ItemPos = None
            while (ItemPos is None or ItemPos.next is not None) and counter < count:
                if ItemPos is None:
                    if starting != "-1":
                        ItemPos = Position.objects.get(list=self, item_id=int(starting))
                    else:
                        listObj = ListModel.objects.get(slug=self.slug)
                        ItemPos = Position.objects.get(list=self, item=listObj.firstItem)
                else:
                    ItemPos = Position.objects.get(list=self, item=ItemPos.next)
                counter += 1
                items.append({
                    "position": counter if starting == "-1" else None,
                    "id": ItemPos.item.id,
                    "item": ItemPos.item,
                    "nextItem": ItemPos.next.id if ItemPos.next else None,
                })
            return items
        except Position.DoesNotExist:
            raise APIException('List item positions cannot be determined.', code='POSITION_CORRUPTED')

    def resolve_itemCount(self, info):
        return len(self.items.all())

    def resolve_userCanEdit(self, info):
        user = info.context.user
        if user.is_authenticated:
            if user == self.curator:
                return True
            if Collaborator.objects.filter(
                    list=self,
                    user=info.context.user
                ).exists():
                return True
        else:
            return False

    def resolve_hasEntries(self, info):
        return ListEntry.objects.filter(
            list=self,
            position__isnull=True
        ).exists()

    def resolve_userVote(self, info):
        if info.context.user.is_authenticated:
            try:
                return ListVote.objects.get(
                    list=self,
                    voter=info.context.user
                ).item
            except ListVote.DoesNotExist:
                return None
        else:
            return None

    def resolve_votes(self, info):
        return ListVote.objects.filter(
            list=self
        )
