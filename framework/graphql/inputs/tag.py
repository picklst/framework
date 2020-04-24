import graphene


class TagInput(graphene.InputObjectType):
    name = graphene.String(required=True)

