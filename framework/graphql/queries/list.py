import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required

from framework.graphql.utils import APIException
from framework.utils.cursor_pagination import CursorPaginator
from list.models import List
from list.utils.decorators import user_can_edit_list
from request.models import ListEntry
from user.models import UserSubscription

from framework.graphql.types import List as ListObj, ListEntry as ListEntryObj
from framework.graphql.inputs import ListQueryInput, ListSelectInput


class ListQuery(graphene.ObjectType):
    lists = graphene.List(ListObj)
    hasNext = graphene.Boolean()
    lastCursor = graphene.String()


class ListEntryQuery(graphene.ObjectType):
    entries = graphene.List(ListEntryObj)
    totalCount = graphene.Int()
    hasNext = graphene.Boolean()
    lastCursor = graphene.String()


class ListQueries(graphene.ObjectType):
    list = graphene.Field(
        ListObj,
        slug=graphene.String(required=True),
        username=graphene.String(required=False)
    )
    lists = graphene.Field(
        ListQuery,
        query=ListQueryInput(required=True),
        count=graphene.Int(),
        after=graphene.String()
    )
    listEntries = graphene.Field(
        ListEntryQuery,
        list=ListSelectInput(required=True),
        count=graphene.Int(),
        after=graphene.String()
    )

    @staticmethod
    def resolve_list(self, info, slug, username=None, **kwargs):
        try:
            if username is not None:
                listObj = List.objects.get(slug=slug, curator__username=username)
            else:
                listObj = List.objects.get(slug=slug)
            if listObj.isActive:
                if not listObj.isPrivate:
                    return listObj
                else:
                    user = info.context.user
                    if user is None:
                        raise APIException("The list is private. Login required to view the list", code='LOGIN_REQUIRED')
                    # @todo check if user is following owner, and owner allowed user
                    try:
                        UserSubscription.objects.get(user=listObj.curator, subscriber=user)
                        return listObj
                    except UserSubscription.DoesNotExist:
                        raise APIException("The list is private, you need to subscription required to view this list", code='NO_SUBSCRIPTION')
            else:
                # @todo find reason and return exact reason for being inactive
                raise APIException("The list has been taken down or removed.", code='LIST_INACTIVE')

        except List.DoesNotExist:
            raise APIException("The list queried does not exit", code='LIST_NOT_FOUND')

    @staticmethod
    def resolve_lists(self, info, query, count=10, after=None, **kwargs):
        if query and query.username is not None:
            username = query.username
        else:
            username = '*'
        qs = List.objects.filter(curator__username=username, isActive=True)
        paginator = CursorPaginator(qs, ordering=('-timestampCreated', '-id'))
        page = paginator.page(first=count, after=after)
        return ListQuery(
            lists=page,
            hasNext=page.has_next,
            lastCursor=paginator.cursor(page[-1]) if page else None
        )

    @login_required
    @user_can_edit_list
    def resolve_listEntries(self, info, list, count=10, after=None):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            qs = ListEntry.objects.filter(
                position__isnull=True,
                list=lists.first()
            )
            resultCount = qs.count()
            paginator = CursorPaginator(qs, ordering=('-timestamp', '-id'))
            page = paginator.page(first=count, after=after)
            return ListEntryQuery(
                entries=page,
                totalCount=resultCount,
                hasNext=page.has_next,
                lastCursor=paginator.cursor(page[-1]) if page else None
            )
        else:
            raise Exception(AttributeError, "Invalid list passed")
