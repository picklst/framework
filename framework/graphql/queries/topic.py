from datetime import datetime

import graphene

from framework.graphql.types import Topic as TopicObj, APIException
from framework.utils.cursor_pagination import CursorPaginator
from taxonomy.models import Topic


class TopicQuery(graphene.ObjectType):
    topics = graphene.List(TopicObj)
    hasNext = graphene.Boolean()
    lastCursor = graphene.String()


class TopicQueries(graphene.ObjectType):
    topic = graphene.Field(TopicObj, slug=graphene.String(required=True))
    topicsFeatured = graphene.Field(TopicQuery, count=graphene.Int(), after=graphene.String())
    topicSearch = graphene.List(TopicObj, query=graphene.String(required=True))

    def resolve_topic(self, info, slug):
        try:
            return Topic.objects.get(slug=slug)
        except Topic.DoesNotExist:
            raise APIException('Topic does not exist', code='DOES_NOT_EXIST')

    @staticmethod
    def resolve_topicsFeatured(self, info, count=10, after=None, **kwargs):
        qs = Topic.objects.all()
        paginator = CursorPaginator(qs, ordering=('-id',))
        page = paginator.page(first=count, after=after)
        return TopicQuery(
            topics=page,
            hasNext=page.has_next,
            lastCursor=paginator.cursor(page[-1]) if page else None
        )

    @staticmethod
    def resolve_topicSearch(self, info, query, **kwargs):
        results = Topic.objects.filter(name__istartswith=query)[:5]
        return results
