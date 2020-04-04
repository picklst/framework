import graphene
from list.api.list.query import Query as ListQueries
from list.api.list.mutation import Mutation as ListMutations
from list.api.item.mutation import Mutation as ItemMutations


class Query(
    ListQueries,
    graphene.ObjectType
):
    pass


class Mutation(
    ListMutations,
    ItemMutations,
    graphene.ObjectType
):
    pass
