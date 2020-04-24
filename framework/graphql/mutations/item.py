import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required

from list.models import List, Item
from log.models import ItemChangeLog

from list.utils.mutations.item import create_item, update_item, delete_item
from list.utils.mutations.list import insert_at_position, move_item_up, move_item_down, exclude_position
from list.utils.decorators import user_can_edit_list

from framework.graphql.utils import APIException
from framework.graphql.inputs import ItemInput, ListSelectInput


class ItemMutationResponse(graphene.ObjectType):
    from framework.graphql.types import Item as ItemObj

    returning = graphene.List(ItemObj)

    def resolve_returning(self, info):
        return self


class ItemCreate(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        objects = graphene.List(ItemInput)

    Output = ItemMutationResponse

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, objects):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            objs = []
            for o in objects:
                o.list = lists.first()
                obj = create_item(o)
                ItemChangeLog.objects.create(
                    user=info.context.user,
                    item=obj
                )
                insert_at_position(obj, o.position)
                objs.append(obj)
            return objs
        raise Exception(AttributeError, "Invalid list passed")


class ItemUpdate(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        objects = graphene.List(ItemInput)

    Output = ItemMutationResponse

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, objects):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            objs = []
            for o in objects:
                o.list = lists.first()
                obj = update_item(o)
                ItemChangeLog.objects.create(
                    user=info.context.user,
                    item=obj
                )
                objs.append(obj)
            return objs
        raise Exception(AttributeError, "Invalid list passed")


class ItemMove(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        direction = graphene.Argument(graphene.Enum('Direction', [('up', 1), ('down', 0)]))
        key = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, direction, key):
        try:
            item = Item.objects.get(key=key)
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
        keys = graphene.List(graphene.String)

    Output = graphene.Boolean

    @login_required
    @user_can_edit_list
    def mutate(self, info, list, keys):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            for k in keys:
                itemObj = Item.objects.get(key=k)
                exclude_position(itemObj)
                delete_item(k)
            return True
        raise Exception(AttributeError, "Invalid list passed")


class ItemMutations(object):
    itemCreate = ItemCreate.Field()
    itemUpdate = ItemUpdate.Field()
    itemMove = ItemMove.Field()
    itemDelete = ItemDelete.Field()
