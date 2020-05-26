from graphql.execution.base import ResolveInfo

from framework.graphql.utils import APIException
from list.models import Collaborator, ItemMedia


def user_can_delete_media(func):
    def wrap(*args, **kwargs):
        info = next(arg for arg in args if isinstance(arg, ResolveInfo))
        user = info.context.user
        mediaID = kwargs.get('id')
        itemMediaObj = ItemMedia.objects.get(media__id=mediaID)
        if itemMediaObj.media.uploader == user:
            return func(*args, **kwargs)
        elif itemMediaObj.item.list.curator == user:
            return func(*args, **kwargs)
        elif Collaborator.objects.filter(list=itemMediaObj.item.list, user=user).exists():
            return func(*args, **kwargs)
        raise APIException('You dont have permission to delete this media', code='PERMISSION_DENIED')
    return wrap

