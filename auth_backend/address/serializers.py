from rest_framework import serializers

from auth_backend.address.models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'id',
            'type',
            'get_type_display',
            'zipcode',
            'place',
            'street',
            'house_num',
            'housing',
            'flat',
        )