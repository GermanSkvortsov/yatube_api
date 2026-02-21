"""Кастомные permissions для API Yatube."""

from rest_framework import permissions


class IsAuthenticatedAuthorOrReadOnly(permissions.BasePermission):
    """
    - Безопасные методы (GET, HEAD, OPTIONS) разрешены всем.
    - Для остальных методов требуется аутентификация и авторство.
    """

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверка прав на уровне конкретного объекта."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
