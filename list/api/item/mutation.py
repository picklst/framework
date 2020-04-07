import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required

from list.utils.mutations.item import create_item
from list.models import List

from list.api.item.objects import ItemObj
from list.api.item.inputs import ItemInput
from list.api.list.inputs import ListSelectInput


class CreateItemObject(graphene.ObjectType):
    returning = graphene.List(ItemObj)

    def resolve_returning(self, info):
        return self


class CreateItem(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        objects = graphene.List(ItemInput)

    Output = CreateItemObject

    @login_required
    def mutate(self, info, list, objects):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            objs = []
            for o in objects:
                o.list = lists.first()
                obj = create_item(o)
                objs.append(obj)
            return objs
        raise Exception(AttributeError, "Invalid list passed")


class Mutation(object):
    createItem = CreateItem.Field()
