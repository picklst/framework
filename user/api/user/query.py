import graphene

from user.models import User


class UserSuggestions(graphene.ObjectType):
    username = graphene.String()
    name = graphene.String()
    avatar = graphene.String()

    def resolve_username(self, info):
        return self['username']

    def resolve_name(self, info):
        return self['first_name'] + ' ' + self['last_name']


class Query(graphene.ObjectType):
    isUsernameAvailable = graphene.Boolean(username=graphene.String(required=True))
    searchUser = graphene.List(UserSuggestions, key=graphene.String(required=True))

    def resolve_isUsernameAvailable(self, info, **kwargs):
        username = kwargs.get('username')
        try:
            User.objects.get(username=username)
            return False
        except User.DoesNotExist:
            return True

    def resolve_searchUser(self, info, **kwargs):
        key = kwargs.get('key')
        results = User.objects.filter(
            username__startswith=key
        ).values(
            'username',
            'first_name',
            'last_name',
            'avatar'
        )
        return results
