import graphene

from framework.graphql.utils import APIException
from list.models import List
from user.models import UserSubscription

from framework.graphql.types import List as ListObj
from framework.graphql.inputs import ListQueryInput


class ListQueries(graphene.ObjectType):
    list = graphene.Field(ListObj, slug=graphene.String(required=True), username=graphene.String(required=False))
    lists = graphene.List(
        ListObj,
        query=ListQueryInput(required=True),
        limit=graphene.Int(),
        offset=graphene.Int()
    )

    @staticmethod
    def resolve_List(self, info, **kwargs):
        slug = kwargs.get('slug')
        username = kwargs.get('username')
        try:
            if username:
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
    def resolve_lists(self, info, query, limit, offset, **kwargs):
        if limit is None:
            limit = 50
        if offset is None:
            offset = 0
        if query and query.username is not None:
            username = query.username
        else:
            username = '*'
        return List.objects.filter(
            curator__username=username
        )[offset:offset + limit]
