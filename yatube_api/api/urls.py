"""URL-маршруты для API Yatube."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # новый импорт

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('follow', FollowViewSet, basename='follow')

posts_router = NestedDefaultRouter(router_v1, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(posts_router.urls)),
]
