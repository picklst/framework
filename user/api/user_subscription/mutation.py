from datetime import datetime

import graphene
from graphql_jwt.decorators import login_required

from framework.utils.graphql import APIException
from user.models import User, UserSubscription


class FollowUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, username):
        if username == info.context.user.username:
            raise APIException('User cannot follow self.', code='CANNOT_FOLLOW_SELF')
        if UserSubscription.objects.filter(user__username=username, subscriber=info.context.user).exists():
            raise APIException('Already following User', code='ALREADY_FOLLOWING_USER')
        else:
            try:
                user = User.objects.get(username=username)
                UserSubscription.objects.create(
                    user=user,
                    subscriber=info.context.user
                )
                return True
            except User.DoesNotExist:
                raise APIException('User does not exist.', code='USER_DOES_NOT_EXIST')


class UnfollowUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, username):
        if UserSubscription.objects.filter(user__username=username, subscriber=info.context.user).exists():
            UserSubscription.objects.get(
                user__username=username,
                subscriber=info.context.user
            ).delete()
            return True
        else:
            raise APIException('User is not being followed.', code='NOT_FOLLOWING_USER')


class Mutation(object):
    followUser = FollowUser.Field()
    unfollowUser = UnfollowUser.Field()
