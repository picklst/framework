import graphene
from urllib.parse import urlparse

from framework.graphql.types import Link as LinkObj
from link.models import Link
from link.utils import fetch_url_meta


class LinkQueries(graphene.ObjectType):
    link = graphene.Field(
        LinkObj,
        url=graphene.String(required=True)
    )

    @staticmethod
    def resolve_link(self, info, url):
        fetchURL = urlparse(url).geturl()
        try:
            link = Link.objects.get(url=url)
            return link
        except Link.DoesNotExist:
            response = fetch_url_meta(fetchURL)
            if response is not None:
                link = Link.objects.create(
                    url=url,
                    title=response['title'],
                    description=response['description'],
                    image=response['image'],
                )
            else:
                link = Link(
                    url=url,
                )
            return link
