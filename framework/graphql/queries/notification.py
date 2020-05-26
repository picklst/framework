from datetime import datetime

import graphene
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django.utils import timezone
from graphql_jwt.decorators import login_required

from framework.graphql.types import Notification as NotificationObj
from framework.utils.cursor_pagination import CursorPaginator

from request.models import FollowUserRequest, ListEntry, ListRequest
from user.models import UserSubscription


class NotificationQuery(graphene.ObjectType):
    hasNext = graphene.Boolean()
    lastCursor = graphene.String()
    notifications = graphene.List(NotificationObj)


class RequestNotifications(graphene.ObjectType):
    listRequests = graphene.Field(
        NotificationQuery,
        count=graphene.Int(),
        after=graphene.String()
    )
    followRequests = graphene.List(NotificationObj)
    listEntries = graphene.List(NotificationObj)

    def resolve_listRequests(self, info, count=10, after=None):
        qs = ListRequest.objects.filter(
            respondent=self,
        )
        paginator = CursorPaginator(qs, ordering=('-timestamp', '-id'))
        page = paginator.page(first=count, after=after)

        requests = list()
        if page.items:
            for i in page.items:
                requests.append({
                    "actor": i.requester.username,
                    "timestamp": i.timestamp,
                    "actionType": "LIST_REQUEST",
                    "actionPhrase": "requested for a list from you",
                    "actionURL": "/new",
                    "resourceTitle": i.subject,
                    "resourceType": "MESSAGE"
                })

        return NotificationQuery(
            notifications=requests,
            hasNext=page.has_next,
            lastCursor=paginator.cursor(page[-1]) if page else None
        )


class ReactionNotifications(graphene.ObjectType):
    startedFollowing = graphene.Field(
        NotificationQuery,
        count=graphene.Int(),
        after=graphene.String()
    )

    def resolve_startedFollowing(self, info, count=10, after=None):
        qs = UserSubscription.objects.filter(
            user=info.context.user
        )
        paginator = CursorPaginator(qs, ordering=('-createdTimestamp', '-id'))
        page = paginator.page(first=count, after=after)

        followers = list()
        if page.items:
            for i in page.items:
                followers.append({
                    "actor": i.subscriber.username,
                    "timestamp": i.createdTimestamp,
                    "actionType": "STARTED_FOLLOWING",
                    "actionPhrase": "started following you",
                    "actionURL": "/"+i.subscriber.username,
                })

        return NotificationQuery(
            notifications=followers,
            hasNext=page.has_next,
            lastCursor=paginator.cursor(page[-1]) if page else None
        )


class UserNotifications(graphene.ObjectType):
    critical = graphene.List(NotificationObj)
    reactions = graphene.Field(ReactionNotifications)
    requests = graphene.Field(RequestNotifications)
    mentions = graphene.List(NotificationObj)
    invites = graphene.List(NotificationObj)

    def resolve_critical(self, info):
        n = list()
        to_tz = timezone.get_default_timezone()
        if not self.isEmailVerified:
            n.append({
                "timestamp": timezone.now().astimezone(to_tz),
                "actionType": "CONFIRM_EMAIL",
                "actionPhrase": "Your email has not been confirmed by us, please check your inbox to verify.",
                "actionURL": None
            })
        return n

    def resolve_reactions(self, info):
        return self

    def resolve_requests(self, info):
        return self


class NotificationQueries(graphene.ObjectType):
    notifications = graphene.Field(UserNotifications)

    @login_required
    def resolve_notifications(self, info, **kwargs):
        return info.context.user
