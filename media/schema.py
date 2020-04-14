import decimal
import uuid

import graphene
from graphql_jwt.decorators import login_required

from framework.utils.graphql import APIException
from media.api.inputs import MediaPropertiesInput
from media.api.objects import MediaObj
from media.models import Media


class MediaUploadObj(graphene.ObjectType):
    returning = graphene.Field(MediaObj)

    def resolve_returning(self, info):
        return self


class UploadMedia(graphene.Mutation):
    class Arguments:
        properties = MediaPropertiesInput()

    Output = MediaUploadObj

    @login_required
    def mutate(self, info, properties):
        if info.context.FILES is not None and 'media' in info.context.FILES:
            user = info.context.user

            key = properties.key if hasattr(properties, "key") and properties.key is not None else uuid.uuid4().hex[:8]
            while Media.objects.filter(key=key).exists():
                key = uuid.uuid4().hex[:8]

            mediaObj = Media.objects.create(
                key=key,
                type=properties.type,
                aspect=decimal.Decimal(properties.aspect),
                uploader=user,
                asset=info.context.FILES['media']
            )
            return mediaObj
        else:
            raise APIException('No file attached', code='FILE_NOT_ATTACHED')


class UploadAvatar(graphene.Mutation):
    Output = graphene.Boolean

    @login_required
    def mutate(self, info):
        if info.context.FILES is not None:
            user = info.context.user
            if 'userAvatar' in info.context.FILES:
                user.avatar = info.context.FILES['userAvatar']
            if 'userCover' in info.context.FILES:
                user.cover = info.context.FILES['userCover']
            user.save()
            return True
        else:
            raise APIException('No file attached', code='FILE_NOT_ATTACHED')


class Mutation(
    graphene.ObjectType
):
    uploadMedia = UploadMedia.Field()
    uploadProfileMedia = UploadAvatar.Field()
