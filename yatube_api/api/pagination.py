"""Кастомные классы пагинации для API Yatube."""

from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class SmartPagination(LimitOffsetPagination):
    """
    Умная пагинация с адаптивным поведением.

    Логика работы:
    - Если в запросе есть параметры limit или offset -> всегда пагинация.
    - Если параметров нет и объектов <= PAGE_SIZE -> обычный список.
    - Если параметров нет и объектов > PAGE_SIZE -> пагинация.
    """

    def paginate_queryset(self, queryset, request, view=None):
        """
        Определяет, нужно ли применять пагинацию к queryset.

        Сохраняет общее количество объектов, request и view для использования
        в get_paginated_response. Принимает решение о пагинации на основе
        наличия параметров запроса и количества объектов.
        """
        self.count = queryset.count()
        self.request = request
        self.view = view

        # Получаем размер страницы из настроек (по умолчанию 10)
        page_size = getattr(settings, 'PAGE_SIZE', 10)

        # Явно запрошенная пагинация через параметры
        if 'limit' in request.query_params or 'offset' in request.query_params:
            return super().paginate_queryset(queryset, request, view)

        # Автоматическая пагинация при большом количестве объектов
        if self.count > page_size:
            return super().paginate_queryset(queryset, request, view)

        # Объектов мало - пагинация не нужна
        return None

    def get_paginated_response(self, data):
        """
        Возвращает либо пагинированный ответ, либо обычный список.

        Если пагинация применялась (есть атрибут count) - возвращает
        стандартный пагинированный ответ. Иначе - просто список данных.
        """
        if not hasattr(self, 'count'):
            return Response(data)
        return super().get_paginated_response(data)
