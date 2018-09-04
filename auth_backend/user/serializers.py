from django.apps import apps
from django.conf import settings
from rest_framework.serializers import ModelSerializer

from auth_backend.role.serializers import OrganizationRoleSerializer


class SimpleUserSerializer(ModelSerializer):
    roles = OrganizationRoleSerializer(many=True)

    class Meta:
        model = apps.get_model(
            *settings.AUTH_USER_MODEL.split('.'))
        fields = (
            'id',
            'email',
            model.USERNAME_FIELD,
            'gender',
            'get_gender_display',
            'birth_date',
            'roles',
        )
