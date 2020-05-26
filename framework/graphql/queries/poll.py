import graphene

from framework.graphql.types.poll import Poll
from framework.graphql.utils import APIException
from list.models import Item
from poll.models import UserPollChoice


class PollQueries(graphene.ObjectType):
    itemPoll = graphene.Field(
        Poll,
        itemID=graphene.String(required=True)
    )

    def resolve_itemPoll(self, info, itemID):
        try:
            item = Item.objects.get(id=itemID)
            if item.pollOptions:
                return Poll(
                    hasAnswer=item.correctOption is not None,
                    totalEntries=UserPollChoice.objects.filter(item=item).count(),
                    options=item.pollOptions.all()
                )
            else:
                raise APIException("Item does not have a poll", code="ITEM_HAS_NO_POLL")
        except Item.DoesNotExist:
            raise APIException("Item does not exist", code="INVALID_ITEM")
