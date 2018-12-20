import operator

from rest_framework import views, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from auth_backend.permission.utils import PermissionRegistry
from auth_backend.role.models import Role
from auth_backend.role.utils import READONLY_ROLE_CODES, get_guest_role
from . import serializers


class PermissionsListView(views.APIView):
    """
    Возвращает список всех доступных прав на ресурсы
    """
    def get(self, request: Request) -> Response:
        resources: dict = {}
        for perm_code in PermissionRegistry.codes():
            name = PermissionRegistry.name_by_code(perm_code)
            (resource_code, _) = perm_code.split(':')
            (resource_name, perm_name) = name.split(':')

            permissions = resources.setdefault(resource_code, {
                "name": resource_name,
                "permissions": []
            })["permissions"]

            permissions.append({
                "code": perm_code,
                "name": perm_name
            })

        sorted_resources = sorted(
            resources.values(),
            key=operator.itemgetter('name'))

        return Response(data=sorted_resources)


class RolesViewSet(viewsets.ModelViewSet):
    """
    CRUD для управления ролями

    list:
    Отображение всех ролей в системе

    create:
    Добавление новой роли

    retrieve:
    Отображение информации о роли

    update:
    Изменение информации о роли

    partial_update:
    Частичное изменение информации о роли

    destroy:
    Удаление роли
    Если у пользователя не осталось роли,
    то он будет перемещен в гостевую роль.
    """
    serializer_class = serializers.FullRoleSerializer
    queryset = Role.objects.all().prefetch_related('permissions').exclude(
        code__in=READONLY_ROLE_CODES
    )

    def perform_destroy(self, instance: Role):
        if instance.code in READONLY_ROLE_CODES:
            raise ValidationError(code="readOnly")

        # Добавить всем пользователям роль Гость, если удаляемая единственная
        users = instance.users.all()
        guest_role = get_guest_role()
        for user in users:
            if user.roles.count() == 1:
                user.roles.add(guest_role)

        super().perform_destroy(instance)
