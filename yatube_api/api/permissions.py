"""Кастомные permissions для API Yatube."""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на уровне запроса и объекта.

    - Безопасные методы (GET, HEAD, OPTIONS) разрешены всем.
    - Для остальных методов требуется аутентификация.
    - Для объектов дополнительно проверяется авторство.
    """

    def has_permission(self, request, view):
        """Проверка прав на уровне запроса."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверка прав на уровне конкретного объекта."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAuthenticatedForFollow(permissions.BasePermission):
    """
    Разрешение для эндпоинта /follow/.

    Доступ только для аутентифицированных пользователей.
    """

    def has_permission(self, request, view):
        """Проверка аутентификации для доступа к подпискам."""
        return request.user and request.user.is_authenticated
