import graphene


from .mutations import (
    AuthorizedMutations,
    CoreMutations,
    ItemMutations,
    ListMutations,
    MediaMutations,
    UserMutations,
)
from .queries import (
    ListQueries,
    UserQueries
)


class Mutation(
    AuthorizedMutations,
    CoreMutations,
    ItemMutations,
    ListMutations,
    MediaMutations,
    UserMutations,
):
    pass


class Query(
    ListQueries,
    UserQueries
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
