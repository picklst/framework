import graphene


class ItemInput(graphene.InputObjectType):
    from taxonomy.api.tag.inputs import TagInput

    name = graphene.String(required=True)
    position = graphene.Int(required=True)
    comment = graphene.String()
    url = graphene.String()
    mentions = graphene.List(TagInput)
    tags = graphene.List(TagInput)
