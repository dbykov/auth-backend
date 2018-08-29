from rest_framework.viewsets import ModelViewSet

from auth_backend.auth.decorators import add_permissions
from auth_backend.permission.models import RolePermission
from auth_backend.permission.serializers import RolePermissionSerializer


@add_permissions
class RolePermissionViewSet(ModelViewSet):
    name = 'role_permission'
    verbose_name = 'Разрешение роли'
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
