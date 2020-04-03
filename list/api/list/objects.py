import graphene


class ListObj(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
