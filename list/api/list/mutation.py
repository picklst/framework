import graphene
from graphql_jwt.decorators import login_required

from list.api.list.inputs import ListInput
from list.api.list.objects import ListObj
from list.utils.mutations.list import create_list, update_list
from log.models import ListChangeLog


class CreateListObject(graphene.ObjectType):
    returning = graphene.List(ListObj)

    def resolve_returning(self, info):
        return self


class CreateList(graphene.Mutation):
    class Arguments:
        objects = graphene.List(ListInput)

    Output = CreateListObject

    @login_required
    def mutate(self, info, objects):
        objs = []
        for o in objects:
            o.user = info.context.user
            obj = create_list(o)
            ListChangeLog.objects.create(
                user=info.context.user,
                list=obj
            )
            objs.append(obj)
        return objs


class UpdateList(graphene.Mutation):
    class Arguments:
        objects = graphene.List(ListInput)

    Output = CreateListObject

    @login_required
    def mutate(self, info, objects):
        objs = []
        for o in objects:
            o.user = info.context.user
            obj = update_list(o)
            ListChangeLog.objects.create(
                user=info.context.user,
                list=obj
            )
            objs.append(obj)
        return objs


class Mutation(object):
    createList = CreateList.Field()
    updateList = UpdateList.Field()
