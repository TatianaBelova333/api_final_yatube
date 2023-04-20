from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (PostViewSet, GroupReadOnlyViewSet,
                       CommentViewSet, FollowListCreateViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupReadOnlyViewSet, basename='groups')
router_v1.register('follow', FollowListCreateViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<post_pk>\d+)/comments/?', CommentViewSet, basename='Comment')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
