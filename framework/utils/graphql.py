from graphene_django.views import GraphQLView as BaseGraphQLView


class GraphQLView(BaseGraphQLView):
    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)
        del formatted_error['locations']
        del formatted_error['path']
        try:
            formatted_error['context'] = error.original_error.context
        except AttributeError:
            pass

        return formatted_error


class APIException(Exception):
    def __init__(self, message, code=None):
        self.context = {}
        if code:
            self.context['code'] = code
        super().__init__(message)
