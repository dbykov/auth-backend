from rest_framework.viewsets import ModelViewSet

from auth_backend.auth.decorators import add_permissions
from auth_backend.roles.serializers import RoleSerializer
from auth_backend.models import Role


@add_permissions
class RoleViewSet(ModelViewSet):
    name = 'role'
    verbose_name = 'Роли пользователей'
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
