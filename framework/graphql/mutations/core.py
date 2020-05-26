import graphene
import graphql_jwt

from framework.graphql.types.user import Profile


class CreateToken(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(
        Profile,
        description="A user instance."
    )

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class CoreMutations(graphene.ObjectType):
    tokenCreate = CreateToken.Field()
    tokenRefresh = graphql_jwt.Refresh.Field()
    tokenVerify = graphql_jwt.Verify.Field()
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()


__all__ = ['CoreMutations']
