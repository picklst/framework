import graphene


class ListSelectInput(graphene.InputObjectType):
    slug = graphene.String()
    id = graphene.Int()


class ListPropertiesInput(graphene.InputObjectType):
    isActive = graphene.Boolean()
    isPrivate = graphene.Boolean()
    isRanked = graphene.Boolean()
    forceCuratorRanking = graphene.Boolean()
    isVotable = graphene.Boolean()
    privateVoting = graphene.Boolean()
    isRateable = graphene.Boolean()
    privateRating = graphene.Boolean()
    enablePublicSuggestion = graphene.Boolean()


class ListInput(graphene.InputObjectType):
    from taxonomy.api.tag.mutation import TagInput
    from list.api.item.inputs import ItemInput

    name = graphene.String(required=True)
    description = graphene.String()
    slug = graphene.String()
    tags = graphene.List(TagInput)
    properties = ListPropertiesInput()
    items = graphene.List(ItemInput)
