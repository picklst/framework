import graphene


class Tag(graphene.ObjectType):
    name = graphene.String()
