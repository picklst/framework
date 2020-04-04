import graphene
from graphql_jwt.decorators import login_required


class UserPublicObj(graphene.ObjectType):
    firstName = graphene.String()
    lastName = graphene.String()
    name = graphene.String()
    username = graphene.String()
    avatarURL = graphene.String()

    def resolve_firstName(self, info):
        return self.first_name

    def resolve_lastName(self, info):
        return self.last_name

    def resolve_name(self, info):
        return self.first_name + ' ' + self.last_name

    def resolve_avatarURL(self, info):
        if self.avatar and hasattr(self.avatar, 'url'):
            return info.context.build_absolute_uri(self.avatar.url)
        return None


class UserProtectedObj(graphene.ObjectType):
    email = graphene.String()


class UserObj(graphene.ObjectType):
    publicInfo = graphene.Field(UserPublicObj)
    protectedInfo = graphene.Field(UserProtectedObj)

    def resolve_publicInfo(self, info):
        return self

    @login_required
    def resolve_protectedInfo(self, info):
        return self

