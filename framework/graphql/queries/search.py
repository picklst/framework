import re
from datetime import datetime
from decimal import Decimal

import graphene
from django.db.models import Q, Value, DecimalField, CharField, IntegerField

from framework.graphql.types import Profile as UserType, List as ListType, Topic as TopicType
from framework.utils.cursor_pagination import CursorPaginator
from list.models import List
from taxonomy.models import Topic
from user.models import User


class Result(graphene.ObjectType):
    position = graphene.Int()
    weight = graphene.Int()


class ListResult(Result, graphene.ObjectType):
    list = graphene.Field(ListType)


class TopicResult(Result, graphene.ObjectType):
    topic = graphene.Field(TopicType)


class UserResult(Result, graphene.ObjectType):
    user = graphene.Field(UserType)


class SearchResults(graphene.ObjectType):
    lists = graphene.List(ListResult)
    users = graphene.List(UserResult)
    topics = graphene.List(TopicResult)


def get_match_percent(string, query):
    try:
        match = len(re.match(query, string, re.I).group(0))
    except:
        match = 0
    return match / len(string) * 100 if len(string) > 0 else 0


class SearchQueries(graphene.ObjectType):
    search = graphene.Field(
        SearchResults,
        query=graphene.String(required=True)
    )

    @staticmethod
    def resolve_search(self, info, query, **kwargs):

        qstr = query.lower()

        # Search List
        listQS = List.objects.filter(
            isActive=True
        ).filter(
            Q(name__istartswith=qstr) |
            Q(topic__name__istartswith=qstr) |
            Q(curator__username__istartswith=qstr)
        )[:100]

        # Search User
        userQS = User.objects.filter(
            is_active=True
        ).filter(
            Q(username__istartswith=qstr) |
            Q(first_name__istartswith=qstr) |
            Q(last_name__istartswith=qstr)
        )[:100]

        # Search Topic
        topicQS = Topic.objects.filter(
            name__istartswith=qstr,
        )[:100]

        listResults = list()
        for i in listQS:
            weight = get_match_percent(i.name, qstr) + get_match_percent(i.curator.username, qstr) * 0.35
            if i.topic:
                weight += get_match_percent(i.topic.name, qstr) * 0.35
            listResults.append({
                "weight": weight,
                "type": "list",
                "object": i,
            })

        userResults = list()
        for i in userQS:
            weight = get_match_percent(i.username, qstr) + get_match_percent(i.first_name, qstr) + get_match_percent(i.last_name, qstr)
            userResults.append({
                "weight": weight,
                "type": "user",
                "object": i,
            })

        topicResults = list()
        for i in topicQS:
            topicResults.append({
                "weight": get_match_percent(i.name, qstr),
                "type": "topic",
                "object": i,
            })

        qs = listResults
        qs += userResults
        qs += topicResults
        qs = sorted(qs, key=lambda i: i['weight'], reverse=True)

        lists = list()
        users = list()
        topics = list()
        position = 1
        for i in qs:
            if i['type'] == 'list':
                lists.append({
                    "position": position,
                    "weight": Decimal(i['weight']).to_integral_value(),
                    "list": i['object']
                })
            elif i['type'] == 'user':
                users.append({
                    "position": position,
                    "weight": Decimal(i['weight']).to_integral_value(),
                    "user": i['object']
                })
            elif i['topic'] == 'topic':
                topics.append({
                    "position": position,
                    "weight": Decimal(i['weight']).to_integral_value(),
                    "topic": i['object']
                })
            position += 1
        return SearchResults(
            lists=lists,
            users=users,
            topics=topics
        )
