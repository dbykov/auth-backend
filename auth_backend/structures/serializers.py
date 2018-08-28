from rest_framework import serializers

from auth_backend.models import StructureType, Structure


class StructireTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name')
        model = StructureType


class StructureSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'type', 'parent')
        model = Structure
