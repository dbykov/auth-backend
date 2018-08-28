from rest_framework.viewsets import ModelViewSet

from auth_backend.auth.serializers import RoleSerializer
from auth_backend.models import Role


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
