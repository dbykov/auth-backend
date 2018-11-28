from rest_framework.viewsets import ModelViewSet

from auth_backend.auth.decorators import add_permissions
from auth_backend.role.serializers import RoleSerializer
from auth_backend.role.models import Role


@add_permissions
class RoleViewSet(ModelViewSet):
    permission_group = 'role'
    verbose_name = 'Роли пользователей'
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
