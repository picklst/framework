import graphene


class ListQueryInput(graphene.InputObjectType):
    username = graphene.String(required=True)


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
    from taxonomy.api.tag.inputs import TagInput
    from list.api.item.inputs import ItemInput

    name = graphene.String(required=True)
    description = graphene.String()
    slug = graphene.String()
    tags = graphene.List(TagInput)
    properties = ListPropertiesInput()
    items = graphene.List(ItemInput)
