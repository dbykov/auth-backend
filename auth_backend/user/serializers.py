from rest_framework.serializers import ModelSerializer

from auth_backend.address.serializers import AddressSerializer
from auth_backend.organization.models import Organization
from auth_backend.role.serializers import RoleSerializer
from auth_backend.user.models import User


class SimpleOrganizationSerializer(ModelSerializer):

    class Meta:
        model = Organization
        fields = (
            'id',
            'short_name',
            'type_id',
            'author_id',
        )


class UserSerializer(ModelSerializer):
    roles = RoleSerializer(many=True)
    address = AddressSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'iname',
            'fname',
            'oname',
            'is_active',
            'is_superuser',
            'gender',
            'get_gender_display',
            'birth_date',
            'roles',
            'phone',
            'address',
        )
