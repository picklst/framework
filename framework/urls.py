from django.contrib import admin
from django.urls import path
from graphql_jwt.decorators import jwt_cookie
from django.views.decorators.csrf import csrf_exempt

from framework.graphql.views import GraphQLPlaygroundView, GraphQLView
from framework.views import HealthCheckView

from django.conf import settings

urlpatterns = [
    path('graphql/', csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=settings.DEBUG)))),
    path('healthz/', HealthCheckView.as_view())
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('playground/', GraphQLPlaygroundView.as_view(endpoint="/api/graphql/")),
    ]
