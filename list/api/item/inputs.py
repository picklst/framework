import graphene


class ItemInput(graphene.InputObjectType):
    from taxonomy.api.tag.mutation import TagInput

    name = graphene.String(required=True)
    position = graphene.Int(required=True)
    comment = graphene.String()
    url = graphene.String()
    tags = graphene.List(TagInput)
