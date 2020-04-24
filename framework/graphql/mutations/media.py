import decimal
import uuid

import graphene
from graphql_jwt.decorators import login_required

from media.models import Media

from framework.graphql.utils import APIException
from framework.graphql.inputs import MediaPropertiesInput
from framework.graphql.types import Media as MediaObj


class MediaUploadResponse(graphene.ObjectType):
    returning = graphene.Field(MediaObj)

    def resolve_returning(self, info):
        return self


class MediaUpload(graphene.Mutation):
    class Arguments:
        properties = MediaPropertiesInput()

    Output = MediaUploadResponse

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


class MediaMutations(graphene.ObjectType):
    mediaUpload = MediaUpload.Field()
