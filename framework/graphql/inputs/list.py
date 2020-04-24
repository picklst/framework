import graphene


class ListSelectInput(graphene.InputObjectType):
    username = graphene.String()
    slug = graphene.String()


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


class ListCreationInput(graphene.InputObjectType):
    from .tag import TagInput
    from .item import ItemInput

    name = graphene.String(required=True)
    description = graphene.String()
    slug = graphene.String()
    tags = graphene.List(TagInput)
    properties = ListPropertiesInput()
    items = graphene.List(ItemInput)


class ListQueryInput(graphene.InputObjectType):
    username = graphene.String(required=True)
