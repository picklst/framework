import graphene
from graphql_jwt.decorators import login_required

from framework.utils.graphql import APIException


class UserStatsObj(graphene.ObjectType):
    listsCreatedCount = graphene.Int()
    followersCount = graphene.Int()
    followingCount = graphene.Int()

    def resolve_listsCreatedCount(self, info):
        from list.models import List
        return List.objects.filter(curator=self).count()

    def resolve_followersCount(self, info):
        from user.models import UserSubscription
        return UserSubscription.objects.filter(user=self).count()

    def resolve_followingCount(self, info):
        from user.models import UserSubscription
        return UserSubscription.objects.filter(subscriber=self).count()


class UserObj(graphene.ObjectType):
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    name = graphene.String()
    isVerified = graphene.Boolean()
    isProfilePrivate = graphene.Boolean()
    isBusinessProfile = graphene.Boolean()
    bio = graphene.String()
    url = graphene.String()
    coverURL = graphene.String()
    avatarURL = graphene.String()
    stats = graphene.Field(UserStatsObj)
    # protected fields
    email = graphene.String()
    followers = graphene.List(lambda: UserObj, limit=graphene.Int(), offset=graphene.Int())
    following = graphene.List(lambda: UserObj, limit=graphene.Int(), offset=graphene.Int())

    def resolve_firstName(self, info):
        return self.first_name

    def resolve_lastName(self, info):
        return self.last_name

    def resolve_name(self, info):
        return self.first_name + ' ' + self.last_name

    def resolve_avatarURL(self, info):
        if self.avatar and hasattr(self.avatar, 'url'):
            return info.context.build_absolute_uri(self.avatar.url)
        return None

    def resolve_coverURL(self, info):
        if self.cover and hasattr(self.cover, 'url'):
            return info.context.build_absolute_uri(self.cover.url)
        return None

    def resolve_stats(self, info):
        return self

    @login_required
    def resolve_email(self, info):
        return self.email

    @login_required
    def resolve_followers(self, info, **kwargs):
        from user.models import UserSubscription

        if not self.isProfilePrivate or UserSubscription.objects.query(user=self, subscriber=info.context.user).exists():
            limit = kwargs.get('limit')
            if limit is None:
                limit = 50
            offset = kwargs.get('offset')
            if offset is None:
                offset = 0
            subs = UserSubscription.objects.filter(user=self).only('subscriber')[offset:offset+limit]
            followersList = []
            for sub in subs:
                followersList.append(sub.subscriber)
            return followersList
        else:
            raise APIException(
                "Profile queried is private, only other followers of the user allowed to view followers list",
                code='NO_SUBSCRIPTION'
            )

    @login_required
    def resolve_following(self, info, **kwargs):
        from user.models import UserSubscription

        if not self.isProfilePrivate or UserSubscription.objects.query(user=self, subscriber=info.context.user).exists():
            limit = kwargs.get('limit')
            if limit is None:
                limit = 50
            offset = kwargs.get('offset')
            if offset is None:
                offset = 0
            follows = UserSubscription.objects.filter(subscriber=self).only('user')[offset:offset + limit]
            followsList = []
            for sub in follows:
                followsList.append(sub.user)
            return followsList
        else:
            raise APIException(
                "Profile queried is private, only followers of the user allowed to view user's following list",
                code='NO_SUBSCRIPTION'
            )
