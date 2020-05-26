import graphene
from django.db.models import F
from graphql_jwt.decorators import login_required

from framework.graphql.types import UserListStory, UserListItemStory, TopicListStory
from framework.utils.cursor_pagination import CursorPaginator
from list.models import List
from user.models import UserSubscription


class PaginationObj(graphene.ObjectType):
    hasNext = graphene.Boolean()
    lastCursor = graphene.String()


class UserCreateListActivity(PaginationObj, graphene.ObjectType):
    stories = graphene.List(UserListStory)


class UserContributeItemActivity(PaginationObj, graphene.ObjectType):
    stories = graphene.List(UserListItemStory)


class TopicNewListActivity(PaginationObj, graphene.ObjectType):
    stories = graphene.List(TopicListStory)


class UserActivities(graphene.ObjectType):
    createList = graphene.Field(
        UserCreateListActivity,
        count=graphene.Int(),
        after=graphene.String()
    )
    contributeItem = graphene.Field(
        UserContributeItemActivity,
        count=graphene.Int(),
        after=graphene.String()
    )
    listVote = graphene.List(UserListItemStory)

    def resolve_createList(self, info, count=10, after=None):
        qs = List.objects.filter(
            isActive=True,
            curator__in=self,
        ).annotate(
            user_id=F('curator'),
            timestamp=F('timestampCreated')
        )
        paginator = CursorPaginator(qs, ordering=('-timestampCreated', '-id'))
        page = paginator.page(first=count, after=after)
        return UserCreateListActivity(
            stories=page,
            hasNext=page.has_next,
            lastCursor=paginator.cursor(page[-1]) if page else None
        )

    def resolve_contributeItem(self, info, count=10, after=None):
        from request.models import ListEntry

        qs = ListEntry.objects.filter(
            contributor__in=self,
            position__isnull=False,
        ).annotate(user_id=F('contributor'))
        paginator = CursorPaginator(qs, ordering=('-timestamp', '-id'))
        page = paginator.page(first=count, after=after)
        return UserContributeItemActivity(
            stories=page,
            hasNext=page.has_next,
            lastCursor=paginator.cursor(page[-1]) if page else None
        )


class TopicActivities(graphene.ObjectType):
    newList = graphene.Field(
        TopicNewListActivity,
        count=graphene.Int(),
        after=graphene.String()
    )


class FeedStories(graphene.ObjectType):
    userActivities = graphene.Field(UserActivities)
    topicActivities = graphene.Field(TopicActivities)

    def resolve_userActivities(self, info):
        followingList = list(UserSubscription.objects.filter(
            subscriber=info.context.user
        ).values_list('user', flat=True))
        followingList.append(info.context.user.id)
        return followingList


class FeedQueries(graphene.ObjectType):
    feed = graphene.Field(FeedStories)

    @login_required
    def resolve_feed(self, info, **kwargs):
        return info.context.user
