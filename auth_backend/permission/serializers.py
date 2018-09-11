from rest_framework.serializers import ModelSerializer

from auth_backend.permission.models import Permission


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'code',
            'name',
        )
