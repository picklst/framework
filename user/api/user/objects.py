import graphene


class UserObj(graphene.ObjectType):
    firstName = graphene.String()
    lastName = graphene.String()
    username = graphene.String()
    email = graphene.String()
    avatarURL = graphene.String()

    def resolve_firstName(self, info):
        return self.first_name

    def resolve_lastName(self, info):
        return self.last_name

    def resolve_avatarURL(self, info):
        if self.avatar is not None:
            return info.context.build_absolute_uri(self.avatar.image.url)
        return None
