from rest_framework.serializers import ModelSerializer

from auth_backend.role.models import Role, OrganizationRole


class RoleSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = ('id', 'code', 'name')


class OrganizationRoleSerializer(ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = OrganizationRole
        fields = (
            'id',
            'role',
            'organization_id',
        )
