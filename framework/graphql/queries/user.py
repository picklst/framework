from datetime import datetime

import graphene
from graphql_jwt.decorators import login_required

from framework.graphql.utils import APIException
from user.models import User

from framework.graphql.types import User as UserObj


class UserQueries(graphene.ObjectType):
    me = graphene.Field(UserObj)
    isUsernameAvailable = graphene.Boolean(
        username=graphene.String(
            description="username to be checked",
            required=True
        ),
        description="Check if an username is already in use or if it is available."
    )
    user = graphene.Field(UserObj, username=graphene.String(required=True))
    userSearch = graphene.List(UserObj, key=graphene.String(required=True))

    @login_required
    def resolve_me(self, info, **kwargs):
        return info.context.user

    @staticmethod
    def resolve_isUsernameAvailable(self, info, username, **kwargs):
        if username is not None and len(username) > 0:
            try:
                User.objects.get(username=username)
                return False
            except User.DoesNotExist:
                return True
        else:
            raise APIException("Invalid username provided", code='INVALID_USERNAME')

    @staticmethod
    def resolve_user(self, info, username, **kwargs):
        print(datetime.now(), username)
        try:
            user = User.objects.get(username=username)
            # @todo check if user is active
            return user
        except User.DoesNotExist:
            raise APIException("The user queried does not exit", code='LIST_NOT_FOUND')

    @staticmethod
    def resolve_userSearch(self, info, key, **kwargs):
        results = User.objects.filter(username__startswith=key)
        return results
