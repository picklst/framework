import graphene
from graphql_jwt.decorators import login_required

from log.models import ListChangeLog
from list.utils.mutations.list import create_list, update_list

from framework.graphql.types import List as ListObj
from framework.graphql.inputs import ListCreationInput


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
        id = graphene.Int(
            description='ID of the list to be updated'
        )
        input = graphene.Argument(
            ListCreationInput,
            description='Fields to be updated in the list'
        )

    Output = ListMutationResponse

    @login_required
    def mutate(self, info, input):
        input.user = info.context.user
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
        id = graphene.Int(
            description='ID of the list to be deleted'
        )

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, input):
        # @todo implement API
        return False


class ListMutations(
    graphene.ObjectType
):
    listCreate = ListCreate.Field()
    listUpdate = ListUpdate.Field()
    listDelete = ListDelete.Field()


__all__ = ['ListMutations']
