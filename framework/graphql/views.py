import json
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.base import TemplateView
from graphene_django.views import GraphQLView as BaseGraphQLView
from graphql_jwt.refresh_token.models import RefreshToken

from user.models import UserSession


class GraphQLView(BaseGraphQLView):
    def dispatch(self, request, *args, **kwargs):
        self.update_session(request)
        response = super().dispatch(request, *args, **kwargs)
        # response = self._delete_cookies_on_response_if_needed(request, response)
        return response

    @staticmethod
    def get_user_agent_data(request):
        userAgent = request.META['HTTP_USER_AGENT']
        from ua_parser import user_agent_parser
        browser = user_agent_parser.ParseUserAgent(userAgent)
        os = user_agent_parser.ParseOS(userAgent)
        device = user_agent_parser.ParseDevice(userAgent)
        return {
            "os": os['family'] or '' + ' ' + os['major'] or '' + '.' + os['minor'] or '',
            "browser": browser['family'] or '' + ' ' + browser['major'] or '',
            "device": device['brand'] or '' + ' ' + device['family'] or '' + ' ' + device['model'] or '',
        }

    def update_session(self, request):
        if 'JWTRefreshToken' in request.COOKIES:
            refreshToken = request.COOKIES["JWTRefreshToken"]
            try:
                rt = RefreshToken.objects.get(token=refreshToken)
                try:
                    session = UserSession.objects.get(refreshToken=rt)
                except UserSession.DoesNotExist:
                    userAgent = self.get_user_agent_data(request)
                    UserSession.objects.create(
                        user=rt.user,
                        refreshToken=rt,
                        ipAddress=request.META['REMOTE_ADDR'],
                        browser=userAgent['browser'],
                        operatingSystem=userAgent['os'],
                        device=userAgent['device']
                    )
            except RefreshToken.DoesNotExist:
                pass
    # def _delete_cookies_on_response_if_needed(self, request, response):
    #     data = self.parse_body(request)
    #     operation_name = self.get_graphql_params(request, data)[2]
    #
    #     if operation_name and operation_name == 'Logout':
    #         response.delete_cookie('JWTAccessToken')
    #         response.delete_cookie('JWTRefreshToken')
    #     return response

    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)
        del formatted_error['locations']
        del formatted_error['path']
        try:
            formatted_error['code'] = error.original_error.code
        except AttributeError:
            pass

        return formatted_error


class GraphQLPlaygroundView(TemplateView):
    template_name = "playground/playground.html"

    endpoint = None
    subscription_endpoint = None
    workspace_name = None
    config = None
    settings = None

    def __init__(self,
                 endpoint=None,
                 subscription_endpoint=None,
                 workspace_name=None,
                 config=None,
                 settings=None,
                 **kwargs):
        super(GraphQLPlaygroundView, self).__init__(**kwargs)
        self.options = {
            'endpoint': endpoint,
            'subscriptionEndpoint': subscription_endpoint,
            'workspaceName': workspace_name,
            'config': config,
            'settings': settings,
        }

    def get_context_data(self, *args, **kwargs):
        context = super(GraphQLPlaygroundView, self).get_context_data(*args, **kwargs)
        context['options'] = json.dumps(self.options, cls=DjangoJSONEncoder)
        return context
