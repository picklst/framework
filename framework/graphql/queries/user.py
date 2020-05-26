import graphene
from django.utils import timezone
from graphql_jwt.decorators import login_required

from framework.graphql.utils import APIException
from user.models import User, UserSubscription, UserInvite

from framework.graphql.types import Profile


class UserQueries(graphene.ObjectType):
    dailySlotsLeft = graphene.Int()
    me = graphene.Field(Profile)
    isUsernameAvailable = graphene.Boolean(
        username=graphene.String(
            description="username to be checked",
            required=True
        ),
        description="Check if an username is already in use or if it is available."
    )
    isFollower = graphene.Boolean(
        username=graphene.String(
            description="username to be checked",
            required=True
        ),
        description="Check if logged-in user is following the given user"
    )
    user = graphene.Field(Profile, username=graphene.String(required=True))
    userSearch = graphene.List(Profile, key=graphene.String(required=True))

    @staticmethod
    def resolve_dailySlotsLeft(self, info):
        today = timezone.now().date()
        return 50 - UserInvite.objects.filter(createdTimestamp__gte=today.isoformat()).count()

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
    def resolve_isFollower(self, info, username):
        try:
            user = User.objects.get(username=username, is_active=True)
            return UserSubscription.objects.filter(
                user=user,
                subscriber=info.context.user
            ).exists()
        except User.DoesNotExist:
            raise APIException("Invalid username provided", code='INVALID_USERNAME')

    @staticmethod
    def resolve_user(self, info, username, **kwargs):
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
