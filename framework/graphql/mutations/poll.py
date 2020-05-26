import graphene
from graphql_jwt.decorators import login_required

from framework.graphql.utils import APIException
from list.models import Item
from poll.models import UserPollChoice, PollOption


class ItemPollSubmitMutation(graphene.Mutation):
    class Arguments:
        optionID = graphene.String(required=True)
        itemID = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, optionID, itemID):
        try:
            item = Item.objects.get(id=itemID)
            try:
                poll = UserPollChoice.objects.get(
                    user=info.context.user,
                    item=item,
                )
                if poll.choice.id != optionID:
                    poll.choice = PollOption.objects.get(id=optionID)
                    poll.save()
                    return True
                else:
                    raise APIException('Already recorded', code="ALREADY_RECORDED")
            except UserPollChoice.DoesNotExist:
                UserPollChoice.objects.create(
                    user=info.context.user,
                    item=item,
                    choice_id=optionID
                )
                return True
        except Item.DoesNotExist:
            raise APIException('Item does not exist.', code='INVALID_ITEM')


class PollQuestionResult(graphene.ObjectType):
    from framework.graphql.types import PollOption as PollOptionType

    isCorrect = graphene.Boolean()
    correctOption = graphene.Field(PollOptionType)


class ItemAnswerSubmitMutation(graphene.Mutation):
    class Arguments:
        optionID = graphene.String(required=True)
        itemID = graphene.String(required=True)

    Output = PollQuestionResult

    def mutate(self, info, optionID, itemID):
        try:
            item = Item.objects.get(id=itemID)
            try:
                optionSelected = PollOption.objects.get(id=optionID)
                if item.correctOption is not None:
                    if item.correctOption == optionSelected:
                        return PollQuestionResult(
                            isCorrect=True,
                            correctOption=item.correctOption
                        )
                    else:
                        return PollQuestionResult(
                            isCorrect=False,
                            correctOption=item.correctOption
                        )
                else:
                    raise APIException('Poll does not have right answer.', code='NO_ANSWER')
            except PollOption.DoesNotExist:
                raise APIException('Option does not exist.', code='INVALID_OPTION')
        except Item.DoesNotExist:
            raise APIException('Item does not exist.', code='INVALID_ITEM')


class PollMutations(
    graphene.ObjectType
):
    itemPollSubmit = ItemPollSubmitMutation.Field()
    itemAnswerSubmit = ItemAnswerSubmitMutation.Field()


__all__ = ['PollMutations']
