import graphene
from graphql_jwt.decorators import login_required

from list.models import ItemMedia, Vote
from log.models import ItemChangeLog
from poll.models import UserPollChoice


class ItemVoteStat(graphene.ObjectType):
    count = graphene.Int()

    def resolve_count(self, info):
        return self.count()


class ItemVote(graphene.ObjectType):
    userVote = graphene.Int()
    score = graphene.Int()
    upVotes = graphene.Field(ItemVoteStat)
    downVotes = graphene.Field(ItemVoteStat)

    def resolve_userVote(self, info):
        if info.context.user.is_authenticated:
            try:
                return -1 if Vote.objects.get(
                    item=self,
                    voter=info.context.user
                ).isNegative else 1
            except Vote.DoesNotExist:
                return 0

    def resolve_score(self, info):
        upVotes = Vote.objects.filter(item=self, isNegative=False).count()
        downVotes = Vote.objects.filter(item=self, isNegative=True).count()
        return upVotes - downVotes

    def resolve_upVotes(self, info):
        return Vote.objects.filter(item=self, isNegative=False)

    def resolve_downVotes(self, info):
        return Vote.objects.filter(item=self, isNegative=True)


class Item(graphene.ObjectType):
    from .media import Media as MediaObj
    from .poll import Poll
    from .user import Profile

    id = graphene.String()
    name = graphene.String()
    comment = graphene.String()
    url = graphene.String()
    media = graphene.Field(MediaObj)
    nextItem = graphene.Field(lambda: Item)
    timestampCreated = graphene.types.DateTime()
    timestampLastEdited = graphene.types.DateTime()
    contributor = graphene.Field(Profile)

    poll = graphene.Field(Poll)
    votes = graphene.Field(ItemVote)

    # def resolve_createdTimestamp(self, info):
    #     log = ItemChangeLog.objects.filter(item=self).order_by('timestamp')
    #     if log.first():
    #         return log.first().timestamp
    #
    # def resolve_lastUpdateTimestamp(self, info):
    #     log = ItemChangeLog.objects.filter(item=self).order_by('-timestamp')
    #     if log.first():
    #         return log.first().timestamp
    def resolve_media(self, info):
        try:
            return ItemMedia.objects.get(item=self).media
        except ItemMedia.DoesNotExist:
            return None
        except ItemMedia.MultipleObjectsReturned:
            return ItemMedia.objects.filter(item=self).first().media

    def resolve_url(self, info):
        return self.url if self.url != '' else None

    def resolve_poll(self, info):
        from .poll import Poll

        options = self.pollOptions.all()
        answer = self.correctOption
        answerID = None

        if self.list.curator == info.context.user:
            answerID = answer.id if answer else None

        totalSubs = None
        if answer is None:
            totalSubs = UserPollChoice.objects.filter(item=self).count()

        userVotedOption = None
        if info.context.user is not None and info.context.user.is_authenticated:
            try:
                userVotedOption = UserPollChoice.objects.get(user=info.context.user, item=self).choice.id
            except UserPollChoice.DoesNotExist:
                pass

        if options.count() > 0:
            return Poll(
                hasAnswer=answer is not None,
                totalEntries=totalSubs,
                userVotedOption=userVotedOption,
                answer=answerID,
                options=options
            )
        else:
            return None

    def resolve_votes(self, info):
        return self
