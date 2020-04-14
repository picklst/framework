import graphene


class MediaObj(graphene.ObjectType):
    key = graphene.String()
    type = graphene.String()
    aspect = graphene.Decimal()
    url = graphene.String()

    def resolve_url(self, info):
        return self.asset.url