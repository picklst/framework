import graphene


class UserProfileInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    firstName = graphene.String()
    lastName = graphene.String()
    bio = graphene.String()
    url = graphene.String()
