import graphene
from graphql_jwt.decorators import login_required

from framework.graphql.utils import APIException
from list.models import List, ListVote
from list.utils.decorators import user_can_edit_list
from log.models import ListChangeLog
from list.utils.mutations.list import create_list, update_list

from framework.graphql.types import List as ListObj
from framework.graphql.inputs import ListCreationInput, ListInput, ListSelectInput


class ListMutationResponse(
    graphene.ObjectType,

):
    returning = graphene.Field(
        ListObj,
        description='List fields to be returned'
    )


class ListCreate(
    graphene.Mutation,
    description='Creates a list'
):
    class Arguments:
        input = graphene.Argument(
            ListCreationInput,
            description='Fields accepted to create a list'
        )

    Output = ListMutationResponse

    @login_required
    def mutate(self, info, input):
        input.user = info.context.user
        obj = create_list(input)
        ListChangeLog.objects.create(
            user=info.context.user,
            list=obj
        )
        return ListMutationResponse(
            returning=obj
        )


class ListUpdate(
    graphene.Mutation,
    description='Updates a list'
):
    class Arguments:
        list = ListSelectInput(required=True)
        input = graphene.Argument(
            ListInput,
            description='Fields to be updated in the list',
            required=True
        )

    Output = ListMutationResponse

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, input, **kwargs):
        input.user = info.context.user
        input.slug = list.slug
        obj = update_list(input)
        ListChangeLog.objects.create(
            user=info.context.user,
            list=obj
        )
        return ListMutationResponse(
            returning=obj
        )


class ListDelete(
    graphene.Mutation,
    description='Deletes a list'
):
    class Arguments:
        list = ListSelectInput(required=True)

    Output = graphene.Boolean

    @login_required
    @user_can_edit_list
    def mutate(self, info, list):
        try:
            listObj = List.objects.get(slug=list.slug)
            listObj.delete()
        except List.DoesNotExist:
            raise APIException('List not found.', code="LIST_DOES_NOT_EXIST")
        return False


class ListCoverUpload(graphene.Mutation):
    class Arguments:
        list = ListSelectInput(required=True)

    Output = graphene.Boolean

    @login_required
    @user_can_edit_list
    def mutate(self, info, list):
        if info.context.FILES is not None:
            if 'cover' in info.context.FILES:
                try:
                    listObj = List.objects.get(slug=list.slug)
                    listObj.cover = info.context.FILES['cover']
                    listObj.save()
                    return True
                except List.DoesNotExist:
                    raise APIException('List not found.', code="LIST_DOES_NOT_EXIST")
            return False
        else:
            raise APIException("File not attached", code="FILE_NOT_ATTACHED")


class ListCoverDelete(graphene.Mutation):
    class Arguments:
        list = ListSelectInput(required=True)

    Output = graphene.Boolean

    @login_required
    @user_can_edit_list
    def mutate(self, info, list):
        try:
            listObj = List.objects.get(slug=list.slug)
            if listObj.cover:
                listObj.cover = None
                listObj.save()
            else:
                raise APIException('List does not have a cover', code="COVER_DOES_NOT_EXITS")
            return True
        except List.DoesNotExist:
            raise APIException('List not found.', code="LIST_DOES_NOT_EXIST")


class ListVoteMutation(graphene.Mutation):
    class Arguments:
        list = ListSelectInput(required=True)
        itemID = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, list, itemID):
        try:
            listObj = List.objects.get(slug=list.slug)
            if listObj.isVotable:
                try:
                    vote = ListVote.objects.get(
                        list=listObj,
                        voter=info.context.user
                    )
                    if vote.item.id == itemID:
                        raise APIException("Already Voted", code='ALREADY_VOTED')
                    else:
                        vote.item_id = itemID
                        vote.save()
                        return True
                except ListVote.DoesNotExist:
                    ListVote.objects.create(
                        list=listObj,
                        voter=info.context.user,
                        item_id=itemID
                    )
                    return True
            else:
                raise APIException("List cannot be voted upon", code="NOT_VOTABLE")
        except List.DoesNotExist:
            raise APIException('List not found.', code="LIST_DOES_NOT_EXIST")


class ListUnvoteMutation(graphene.Mutation):
    class Arguments:
        list = ListSelectInput(required=True)
        itemID = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, list, itemID):
        try:
            listObj = List.objects.get(slug=list.slug)
            if listObj.isVotable:
                try:
                    ListVote.objects.get(
                        list=listObj,
                        voter=info.context.user,
                        item_id=itemID
                    ).delete()
                except ListVote.DoesNotExist:
                    raise APIException("User has not voted", code="NOT_VOTED")
            else:
                raise APIException("List cannot be voted upon", code="NOT_VOTABLE")
        except List.DoesNotExist:
            raise APIException('List not found.', code="LIST_DOES_NOT_EXIST")


class ListMutations(
    graphene.ObjectType
):
    listCreate = ListCreate.Field()
    listUpdate = ListUpdate.Field()
    listDelete = ListDelete.Field()
    listCoverUpload = ListCoverUpload.Field()
    listCoverDelete = ListCoverDelete.Field()
    listVote = ListVoteMutation.Field()
    listUnvote = ListUnvoteMutation.Field()


__all__ = ['ListMutations']
