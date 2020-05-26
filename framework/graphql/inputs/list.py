import graphene


class ListSelectInput(graphene.InputObjectType):
    slug = graphene.String()
    id = graphene.Int()


class ListPropertiesInput(graphene.InputObjectType):
    isPrivate = graphene.Boolean()
    isRanked = graphene.Boolean()
    forceCuratorRanking = graphene.Boolean()
    isVotable = graphene.Boolean()
    areVotesPrivate = graphene.Boolean()
    canVoteMultipleItems = graphene.Boolean()
    isRateable = graphene.Boolean()
    areRatingsPrivate = graphene.Boolean()
    acceptEntries = graphene.Boolean()


class ListInput(graphene.InputObjectType):
    from .tag import TagInput

    name = graphene.String()
    description = graphene.String()
    slug = graphene.String()
    topic = graphene.String()
    tags = graphene.List(TagInput)
    properties = ListPropertiesInput()


class ListCreationInput(ListInput):
    from .item import ItemInput

    name = graphene.String(required=True)
    items = graphene.List(ItemInput)


class ListQueryInput(graphene.InputObjectType):
    username = graphene.String(required=True)
