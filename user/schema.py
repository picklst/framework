import graphene
from user.api.user.query import Query as UserQueries
from user.api.user.mutation import Mutation as UserMutations

from user.api.user_subscription.query import Query as SubscriptionQueries
from user.api.user_subscription.mutation import Mutation as SubscriptionMutations


class Query(
    UserQueries,
    SubscriptionQueries,
    graphene.ObjectType
):
    pass


class Mutation(
    UserMutations,
    SubscriptionMutations,
    graphene.ObjectType
):
    pass
