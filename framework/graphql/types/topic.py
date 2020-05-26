import graphene


class Topic(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
    previewURL = graphene.String()
    listsCount = graphene.Int()

    def resolve_listsCount(self, info):
        from list.models import List

        return List.objects.filter(topic=self).count()

    def resolve_previewURL(self, info):
        return '/topic/' + self.slug
