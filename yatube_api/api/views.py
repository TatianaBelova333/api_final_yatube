from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins

from posts.models import Group, Follow, Post
from api.serializers import (PostSerializer, GroupSerializer,
                             CommentSerializer, FollowSerializer)
from api.permissions import IsObjAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Viewset for retrieving and editing Post instances."""
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsObjAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for retrieving a list of groups or a single group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for retrieving and editing Comment instances."""
    serializer_class = CommentSerializer
    permission_classes = (IsObjAuthorOrReadOnly,)

    def _get_post(self):
        post_id = self.kwargs.get('post_pk')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self, *args, **kwargs):
        post = self._get_post()
        return post.comments.select_related('post', 'author').all()

    def perform_create(self, serializer):
        post = self._get_post()
        serializer.save(author=self.request.user, post=post)


class ListCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowListCreateViewSet(ListCreateViewSet):
    """
    Viewset for viewing a list of users followed by the request user
    and adding new users to the request user's subscriptions.

    """
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self, *args, **kwargs):
        queryset = Follow.objects.select_related('user', 'following').all()
        return queryset.filter(user=self.request.user)
