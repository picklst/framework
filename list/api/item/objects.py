import graphene


class ItemObj(graphene.ObjectType):
    name = graphene.String()
    key = graphene.String()
    comment = graphene.String()
    url = graphene.String()