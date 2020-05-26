import graphene


class ListEntry(graphene.ObjectType):
    from .user import Profile
    from .item import Item

    id = graphene.String()
    contributor = graphene.Field(Profile)
    item = graphene.Field(Item)
    timestamp = graphene.String()
