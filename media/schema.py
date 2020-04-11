import graphene
from graphql_jwt.decorators import login_required

from framework.utils.graphql import APIException

MediaUploadTypeEnum = graphene.Enum(
    'MediaUploadType',
    [
        ('userAvatar', 1),
        ('profileCover', 2)
    ])


class UploadMedia(graphene.Mutation):
    class Arguments:
        type = MediaUploadTypeEnum()

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, type):
        if info.context.FILES is not None:
            if type == 1 and 'userAvatar' in info.context.FILES:
                user = info.context.user
                user.avatar = info.context.FILES['userAvatar']
                user.save()
                return True
        raise APIException('No file attached', code='FILE_NOT_ATTACHED')


class Mutation(
    graphene.ObjectType
):
    uploadMedia = UploadMedia.Field()
