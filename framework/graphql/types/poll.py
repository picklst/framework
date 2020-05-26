import graphene

from poll.models import UserPollChoice


class PollOption(graphene.ObjectType):
    from .media import Media

    id = graphene.String()
    name = graphene.String()
    media = graphene.Field(Media)
    votes = graphene.Int()

    def resolve_votes(self, info):
        return UserPollChoice.objects.filter(choice=self).count()


class Poll(graphene.ObjectType):
    hasAnswer = graphene.Boolean()
    answer = graphene.String()
    totalEntries = graphene.Int()
    userVotedOption = graphene.String()
    options = graphene.List(PollOption)
