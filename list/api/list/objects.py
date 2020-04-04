import graphene


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
    description = graphene.String()
    properties = graphene.Field(ListPropertiesObj)
    tags = graphene.List(TagObj)
    items = graphene.List(PositionResolvedItemObj)

    def resolve_properties(self, info):
        return self

    def resolve_items(self, info):
        from list.models import Position
        return Position.objects.filter(list=self).order_by('position')
