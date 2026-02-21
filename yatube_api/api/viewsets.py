"""Базовые классы вьюсетов для API Yatube."""

from rest_framework import viewsets


class BasePostViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет для постов с пагинацией."""

    pass
