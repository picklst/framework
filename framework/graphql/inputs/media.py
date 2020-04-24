import graphene


class MediaPropertiesInput(graphene.InputObjectType):
    key = graphene.String()
    aspect = graphene.String()
    type = graphene.String()
