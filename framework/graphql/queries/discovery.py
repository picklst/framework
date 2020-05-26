import graphene
from django.db.models import Q

from curation.models import FeaturedList as FeaturedListModel
from framework.graphql.inputs import ListSelectInput
from framework.graphql.types import List as ListType
from framework.graphql.utils import APIException
from list.models import List


class FeaturedList(graphene.ObjectType):
    list = graphene.Field(ListType)
    timestamp = graphene.String()


class DiscoveryQueries(graphene.ObjectType):
    featuredLists = graphene.List(
        FeaturedList,
    )
    relatedLists = graphene.List(
        ListType,
        list=ListSelectInput(required=True)
    )

    @staticmethod
    def resolve_featuredLists(self, info):
        return FeaturedListModel.objects.all().order_by('-timestamp')[:6]

    @staticmethod
    def resolve_relatedLists(self, info, list):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)))
        if lists.count() == 1:
            l = lists.first()
            relatedListByUser = List.objects.filter(
                Q(curator=l.curator)
            ).exclude(id=l.id)
            relatedListByTopics = List.objects.filter(
                Q(topic=l.topic)
            ).exclude(id=l.id)
            qs = relatedListByUser.intersection(relatedListByTopics)
            if qs.count() < 5:
                qs = qs.union(relatedListByTopics)
            if qs.count() < 5:
                qs = qs.union(relatedListByUser)
            return qs[:5]
        else:
            raise APIException('Invalid list passed', code="INVALID_LIST")

