import graphene
from django.db.models import Count


class ItemVoteStats(graphene.ObjectType):
    from .item import Item

    item = graphene.Field(Item)
    votes = graphene.Int()

    def resolve_item(self, info):
        from list.models import Item
        return Item.objects.get(id=self['item__id'])

    def resolve_votes(self, info):
        return self['id__count']


class ListVoteStats(graphene.ObjectType):
    totalVotes = graphene.Int()
    rankList = graphene.List(ItemVoteStats)

    def resolve_totalVotes(self, info):
        return self.count()

    def resolve_rankList(self, info):
        return self.values('item__id').annotate(Count('id'))
