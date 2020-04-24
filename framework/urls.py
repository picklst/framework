from django.contrib import admin
from django.urls import path
from graphql_jwt.decorators import jwt_cookie
from django.views.decorators.csrf import csrf_exempt

from framework.graphql.views import GraphQLPlaygroundView, GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=False)))),
    path('playground/', GraphQLPlaygroundView.as_view(endpoint="/api/graphql/")),
]
