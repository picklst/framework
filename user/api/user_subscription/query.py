import graphene
from graphql_jwt.decorators import login_required

from framework.utils.graphql import APIException
from user.models import UserSubscription


class Query(graphene.ObjectType):
    isFollower = graphene.Boolean(username=graphene.String(required=True))

    @login_required
    def resolve_followsUser(self, info, **kwargs):
        username = kwargs.get('username')
        try:
            UserSubscription.objects.get(user__username=username, subscriber=info.context.user)
            return True
        except UserSubscription.DoesNotExist:
            return False
