import graphene


class ItemInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    position = graphene.Int()
    key = graphene.String()
    comment = graphene.String()
    url = graphene.String()
    mentions = graphene.List(graphene.String)
    tags = graphene.List(graphene.String)
    media = graphene.String()
