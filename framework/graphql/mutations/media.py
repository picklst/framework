import decimal

import graphene
from graphql_jwt.decorators import login_required

from media.models import Media

from framework.graphql.utils import APIException
from framework.graphql.inputs import MediaPropertiesInput
from framework.graphql.types import Media as MediaObj
from media.utils.decorators import user_can_delete_media


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
            return Media.objects.create(
                type=properties.type,
                aspect=decimal.Decimal(properties.aspect),
                uploader=user,
                asset=info.context.FILES['media']
            )
        else:
            raise APIException('No file attached', code='FILE_NOT_ATTACHED')


class MediaDelete(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    Output = graphene.Boolean

    @login_required
    @user_can_delete_media
    def mutate(self, info, id):
        Media.objects.get(id=id).delete()
        return True


class MediaMutations(graphene.ObjectType):
    mediaUpload = MediaUpload.Field()
    mediaDelete = MediaDelete.Field()
