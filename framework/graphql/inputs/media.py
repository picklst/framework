import graphene


class MediaPropertiesInput(graphene.InputObjectType):
    aspect = graphene.String()
    type = graphene.String()
