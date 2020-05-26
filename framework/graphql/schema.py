import graphene


from .mutations import (
    AuthorizedMutations,
    CoreMutations,
    ItemMutations,
    ListMutations,
    MediaMutations,
    PollMutations,
    RequestMutations,
    ReportMutations,
    TopicMutations,
    UserMutations,
)
from .queries import (
    DiscoveryQueries,
    FeedQueries,
    LinkQueries,
    ListQueries,
    NotificationQueries,
    PollQueries,
    TopicQueries,
    SearchQueries,
    UserQueries,
)


class Mutation(
    AuthorizedMutations,
    CoreMutations,
    ItemMutations,
    ListMutations,
    MediaMutations,
    PollMutations,
    RequestMutations,
    ReportMutations,
    TopicMutations,
    UserMutations,
):
    pass


class Query(
    DiscoveryQueries,
    FeedQueries,
    LinkQueries,
    ListQueries,
    NotificationQueries,
    PollQueries,
    TopicQueries,
    SearchQueries,
    UserQueries
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
