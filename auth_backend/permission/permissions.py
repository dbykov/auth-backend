from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAuthor(BasePermission):
    """
    Проверка пользователя на авторство над указанным объектом
    """

    def has_object_permission(
            self, request: Request, view: Any, obj: Any) -> bool:
        return obj.is_owned_by(request.user)


class HasRolePermission(BasePermission):
    """
    Проверка наличия у роли пользователя разрешения с требуемым кодом
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        return self._check_permission(request, view)

    def _check_permission(self, request: Request, view: Any) -> bool:
        if request.user.is_anonymous:
            return False

        method_conformity = {
            'get': 'retrieve',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }

        result = False
        # Если декоратор `add_permissions` не используется,
        # то доступ всегда запрещен
        if not hasattr(view, '_wrappers'):
            return False

        method = request.method.lower()
        wrapper_data = view._wrappers.get(method)
        if wrapper_data is None and method in method_conformity:
            wrapper_data = view._wrappers.get(method_conformity[method])

        # Если данный конкретный метод не обернут декоратором,
        # то доступ разрешен
        if wrapper_data is None:
            result = True
        # Проверка ролей пользователя
        elif request.user.has_permission(wrapper_data.permissions):
            result = True

        return result
