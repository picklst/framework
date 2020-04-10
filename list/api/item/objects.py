import graphene


class ItemObj(graphene.ObjectType):
    name = graphene.String()
    key = graphene.String()
    comment = graphene.String()
    url = graphene.String()
    nextItem = graphene.Field(lambda: ItemObj)


class PositionResolvedItemObj(ItemObj):
    position = graphene.Int()

    def resolve_name(self, info):
        return self['item'].name

    def resolve_key(self, info):
        return self['item'].key

    def resolve_comment(self, info):
        return self['item'].comment

    def resolve_url(self, info):
        return self['item'].url

    def resolve_nextItem(self, info):
        return self['nextItem']

    def resolve_position(self, info):
        return self['position']
