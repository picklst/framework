import graphene


class ItemInput(graphene.InputObjectType):
    from .poll import PollInput

    name = graphene.String(required=True)
    position = graphene.Int()
    comment = graphene.String()
    url = graphene.String()
    mentions = graphene.List(graphene.String)
    tags = graphene.List(graphene.String)
    poll = graphene.InputField(PollInput)
    mediaID = graphene.String()
