import graphene


class Embed(graphene.ObjectType):
    provider = graphene.String()
    contentID = graphene.String()
    contentType = graphene.String()


class Link(graphene.ObjectType):
    url = graphene.String()
    title = graphene.String()
    description = graphene.String()
    image = graphene.String()

    embed = graphene.Field(Embed)

    def resolve_embed(self, info):
        from link.utils import get_embed_from_url

        return get_embed_from_url(self.url)
