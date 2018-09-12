from rest_framework.viewsets import ModelViewSet

from auth_backend.auth.decorators import add_permissions
from auth_backend.permission.models import Permission
from auth_backend.permission.serializers import PermissionSerializer


@add_permissions
class PermissionViewSet(ModelViewSet):
    name = 'permission'
    verbose_name = 'Разрешение роли'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
