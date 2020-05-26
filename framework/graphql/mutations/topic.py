import graphene
from django.utils.text import slugify
from graphql_jwt.decorators import login_required

from framework.graphql.types import Topic as TopicType
from taxonomy.models import Topic


class TopicCreationResponse(graphene.ObjectType):
    returning = graphene.Field(TopicType)


class TopicCreateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    Output = TopicCreationResponse

    @login_required
    def mutate(self, info, name):
        topic = Topic.objects.create(
            name=name,
            slug=slugify(name)
        )
        return TopicCreationResponse(
            returning=topic
        )


class TopicMutations(
    graphene.ObjectType
):
    topicCreate = TopicCreateMutation.Field()


__all__ = ['TopicMutations']
