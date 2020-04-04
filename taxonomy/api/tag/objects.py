import graphene


class TagObj(graphene.ObjectType):
    name = graphene.String()
