from rest_framework.serializers import ModelSerializer

from auth_backend.address.serializers import AddressSerializer
from auth_backend.organization.models import (
    OrganizationType, Organization)
from auth_backend.user.serializers import SimpleUserSerializer


class OrganizationTypeSerializer(ModelSerializer):

    class Meta:
        model = OrganizationType
        fields = (
            'id',
            'name',
        )


class OrganizationSerializer(ModelSerializer):
    address_jur = AddressSerializer()
    address_fact = AddressSerializer()
    boss = SimpleUserSerializer()

    class Meta:
        model = Organization
        fields = (
            'id',
            'full_name',
            'short_name',
            'type',
            'parent_id',
            'inn',
            'kpp',
            'okato',
            'license',
            'boss',
            'address_jur',
            'address_fact',
            'phone',
            'email',
            'site',
        )
