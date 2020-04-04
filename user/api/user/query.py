import graphene

from framework.utils.graphql import APIException
from user.api.user.objects import UserObj, UserPublicObj
from user.models import User


class Query(graphene.ObjectType):
    getUser = graphene.Field(UserObj, username=graphene.String(required=True))
    isUsernameAvailable = graphene.Boolean(username=graphene.String(required=True))
    searchUser = graphene.List(UserPublicObj, key=graphene.String(required=True))

    def resolve_getUser(self, info, **kwargs):
        username = kwargs.get('username')
        try:
            user = User.objects.get(username=username)
            # @todo check if user is active
            return user
        except User.DoesNotExist:
            raise APIException("The user queried does not exit", code='LIST_NOT_FOUND')

    def resolve_isUsernameAvailable(self, info, **kwargs):
        username = kwargs.get('username')
        try:
            User.objects.get(username=username)
            return False
        except User.DoesNotExist:
            return True

    def resolve_searchUser(self, info, **kwargs):
        key = kwargs.get('key')
        results = User.objects.filter(username__startswith=key)
        return results
