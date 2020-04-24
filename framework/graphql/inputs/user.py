import graphene


class UserCreationInput(graphene.InputObjectType):
    email = graphene.String(required=True, description='Email address of the user')
    password = graphene.String(description='Login password for the user')
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()


class UserUpdationInput(graphene.InputObjectType):
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    bio = graphene.String()
    url = graphene.String()
