"""ViewSets для API Yatube."""

from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets

from posts.models import Comment, Follow, Group, Post
from .pagination import SmartPagination
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedForFollow
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = SmartPagination

    def perform_create(self, serializer):
        """Автоматически подставляем автора при создании поста."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = SmartPagination

    def get_queryset(self):
        """Фильтруем комментарии по post_id из URL."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        """
        Автоматически подставляем автора и пост при создании комментария.
        """
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = SmartPagination


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с подписками."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedForFollow]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    pagination_class = SmartPagination

    def get_queryset(self):
        """Возвращаем только подписки текущего пользователя."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Автоматически подставляем пользователя при создании подписки."""
        serializer.save(user=self.request.user)
