from graphql.execution.base import ResolveInfo

from framework.graphql.utils import APIException
from list.models import List, Collaborator


def user_can_edit_list(func):
    def wrap(*args, **kwargs):
        info = next(arg for arg in args if isinstance(arg, ResolveInfo))
        user = info.context.user
        slug = kwargs.get('list').get('slug')
        listObj = List.objects.get(slug=slug)
        if listObj.curator == user:
            return func(*args, **kwargs)
        elif Collaborator.objects.filter(list=listObj, user=user).exists():
            return func(*args, **kwargs)
        raise APIException('You dont have permission to make changes to this list', code='PERMISSION_DENIED')
    return wrap


def list_accepts_entries(func):
    def wrap(*args, **kwargs):
        slug = kwargs.get('list').get('slug')
        listObj = List.objects.get(slug=slug)
        if listObj.acceptEntries:
            return func(*args, **kwargs)
        raise APIException('You cannot make contributions to this list', code='ENTRIES_NOT_ACCEPTED')
    return wrap
