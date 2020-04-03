import graphene
from list.api.list.mutation import Mutation as ListMutations
from list.api.item.mutation import Mutation as ItemMutations


class Query(
    graphene.ObjectType
):
    version = graphene.Boolean()


class Mutation(
    ListMutations,
    ItemMutations,
    graphene.ObjectType
):
    pass
