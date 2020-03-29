import graphene
from user.api.user.query import Query as UserQueries
from user.api.user.mutation import Mutation as UserMutations


class Query(
    UserQueries,
    graphene.ObjectType
):
    version = graphene.Boolean()


class Mutation(
    UserMutations,
    graphene.ObjectType
):
    pass
