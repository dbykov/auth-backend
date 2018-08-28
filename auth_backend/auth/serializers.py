from rest_framework.serializers import ModelSerializer

from auth_backend.models import Role


class RoleSerializer(ModelSerializer):

    class Meta:
        model = Role
        fields = ('code', 'name')
