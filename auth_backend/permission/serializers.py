from rest_framework.serializers import ModelSerializer

from auth_backend.organization.serializers import OrganizationSerializer
from auth_backend.permission.models import RolePermission, MetaPermission


class MetaPermissionSerializer(ModelSerializer):
    class Meta:
        model = MetaPermission
        fields = (
            'id',
            'code',
            'name',
        )


class RolePermissionSerializer(ModelSerializer):
    organizations = OrganizationSerializer(many=True)
    meta_permission = MetaPermissionSerializer()

    class Meta:
        model = RolePermission
        fields = (
            'id',
            'code',
            'name',
            'meta_permission',
            'organizations',
            'author',
        )
