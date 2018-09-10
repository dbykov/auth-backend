from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthor(BasePermission):
    """
    Проверка пользователя на авторство над указанным объектом
    """

    def has_object_permission(
            self, request: Request, viewset: APIView, obj: Any) -> bool:
        return obj.is_owned_by(request.user)


class HasRolePermission(BasePermission):
    """
    Проверка наличия у роли пользователя разрешения с требуемым кодом
    """

    def has_permission(self, request, view):
        return self._check_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return self._check_permission(request, view)

    def _check_permission(self, request, view):
        result = False
        # Если декоратор `add_permissions` не используется,
        # то доступ всегда разрешен
        if not hasattr(view, '_wrappers'):
            return True

        method = request.method.lower()
        wrapper_data = view._wrappers.get(method)

        # Если данный конкретный метод не обернут декоратором,
        # то доступ разрешен
        if wrapper_data is None:
            result = True
        # Проверка ролей пользователя
        elif request.user.has_permission(wrapper_data.full_code):
            result = True

        return result
