import graphene
from django.utils import timezone

from user.models import User


class Story(graphene.ObjectType):
    timestamp = graphene.String()

    def resolve_timestamp(self, info):
        to_tz = timezone.get_default_timezone()
        return self.timestamp.astimezone(to_tz)


class ListStory(Story):
    from .list import List as ListType

    list = graphene.Field(ListType)

    def resolve_list(self, info):
        if not hasattr(self, "list") or self.list is None:
            return self
        else:
            return self.list


class UserListStory(ListStory):
    from .user import Profile

    user = graphene.Field(Profile)

    def resolve_user(self, info):
        if not hasattr(self, "user") or self.user is None:
            if hasattr(self, "user_id") and self.user_id is not None:
                return User.objects.get(id=self.user_id)
        else:
            return self.user


class UserListItemStory(UserListStory):
    from .item import Item

    item = graphene.Field(Item)


class TopicListStory(ListStory):
    from .topic import Topic

    topic = graphene.Field(Topic)


