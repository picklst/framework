import graphene
from user.models import User


class Query(graphene.ObjectType):
    isUsernameAvailable = graphene.Boolean(username=graphene.String(required=True))

    @staticmethod
    def resolve_isUsernameAvailable(self, info, **kwargs):
        username = kwargs.get('username')
        try:
            User.objects.get(username=username)
            return False
        except User.DoesNotExist:
            return True
