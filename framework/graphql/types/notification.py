from datetime import datetime

import graphene

from framework.graphql.types import Profile

from user.models import User

#
#   [ACTOR] {ACTION} [Resource]
#   <a>Actor</a> <a>Action</a> +  eg: Actor has requested to follow you. Opens Acceptor Module
#   <a>Actor<a> + Action eg: actor started following you
#   <a>Action</a>  eg:  please verify your email address
#   <a><a>Actor</a>
#


class Action(graphene.ObjectType):
    phrase = graphene.String()
    type = graphene.String()
    url = graphene.String()


class Resource(graphene.ObjectType):
    title = graphene.String()
    type = graphene.String()
    url = graphene.String()


class Notification(graphene.ObjectType):
    timestamp = graphene.String()
    actor = graphene.Field(Profile)
    action = graphene.Field(Action)
    resource = graphene.Field(Resource)

    def resolve_actor(self, info):
        if 'actor' in self:
            return User.objects.get(username=self['actor'])

    def resolve_action(self, info):
        if 'actionPhrase' in self or 'actionType' in self or 'actionURL' in self:
            return {
                'phrase': self['actionPhrase'] if 'actionPhrase' in self else None,
                'type': self['actionType'] if 'actionType' in self else None,
                'url': self['actionURL'] if 'actionURL' in self else None,
            }

    def resolve_resource(self, info):
        if 'resourceTitle' in self or 'resourceType' in self or 'resourceURL' in self:
            return {
                'title': self['resourceTitle'] if 'resourceTitle' in self else None,
                'type': self['resourceType'] if 'resourceType' in self else None,
                'url': self['resourceURL'] if 'resourceURL' in self else None
            }