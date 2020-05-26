import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required

from list.models import List, Item, Vote
from log.models import ItemChangeLog

from list.utils.mutations.item import create_item, update_item, delete_item
from list.utils.mutations.list import insert_at_position, move_item_up, move_item_down, exclude_position
from list.utils.decorators import user_can_edit_list, list_accepts_entries

from framework.graphql.utils import APIException
from framework.graphql.inputs import ItemInput, ListSelectInput


class ItemMutationResponse(graphene.ObjectType):
    from framework.graphql.types import Item as ItemObj
    returning = graphene.Field(ItemObj)

    def resolve_returning(self, info):
        return self


class ItemCreate(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        object = graphene.Argument(ItemInput, required=True)

    Output = ItemMutationResponse

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, object):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            object.list = lists.first()
            obj = create_item(object)
            ItemChangeLog.objects.create(
                user=info.context.user,
                item=obj
            )
            insert_at_position(obj, object.position)
            return obj
        else:
            raise Exception(AttributeError, "Invalid list passed")


class ItemUpdate(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        id = graphene.String(required=True)
        object = graphene.Argument(ItemInput, required=True)

    Output = ItemMutationResponse

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, id, object):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            object.list = lists.first()
            object.id = id
            obj = update_item(object)
            ItemChangeLog.objects.create(
                user=info.context.user,
                item=obj
            )
            return obj
        else:
            raise Exception(AttributeError, "Invalid list passed")


class ItemMove(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        direction = graphene.Argument(graphene.Enum('Direction', [('up', 1), ('down', 0)]))
        id = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, direction, id):
        try:
            item = Item.objects.get(id=id)
            if direction == 1:
                return move_item_up(item)
            elif direction == 0:
                return move_item_down(item)
            else:
                raise APIException('Direction should be either up or down', code='INVALID_DIRECTION')
        except Item.DoesNotExist:
            raise APIException('Item with the provided key does not exist.', code='ITEM_DOES_NOT_EXIST')
        except Item.MultipleObjectsReturned:
            # @todo report incident
            raise APIException('Database Integrity Error, multiple items with same key found.', code='DATABASE_ERROR')


class ItemDelete(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        id = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, id):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            itemObj = Item.objects.get(id=id)
            exclude_position(itemObj)
            delete_item(id)
            return True
        else:
            raise Exception(AttributeError, "Invalid list passed")


class ItemVote(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        isNegative = graphene.Boolean()

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, id, isNegative):
        try:
            itemObj = Item.objects.get(id=id)
            try:
                vote = Vote.objects.get(
                    item=itemObj,
                    voter=info.context.user
                )
                if vote.isNegative == isNegative:
                    return True
                else:
                    vote.isNegative = isNegative
                    vote.save()
                    return True
            except Vote.DoesNotExist:
                Vote.objects.create(
                    item=itemObj,
                    voter=info.context.user,
                    isNegative=isNegative
                )
                return True
        except Item.DoesNotExist:
            raise APIException('Item does not exist', code='ITEM_DOES_NOT_EXIST')


class ItemUnvote(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, id):
        try:
            itemObj = Item.objects.get(id=id)
            try:
                Vote.objects.get(
                    item=itemObj,
                    voter=info.context.user
                ).delete()
                return True
            except Vote.DoesNotExist:
                raise APIException('Vote does not exist', code='VOTE_DOES_NOT_EXIST')
        except Item.DoesNotExist:
            raise APIException('Item does not exist', code='ITEM_DOES_NOT_EXIST')


class ItemMutations(object):
    itemCreate = ItemCreate.Field()
    itemUpdate = ItemUpdate.Field()
    itemMove = ItemMove.Field()
    itemDelete = ItemDelete.Field()
    itemVote = ItemVote.Field()
    itemUnvote = ItemUnvote.Field()
