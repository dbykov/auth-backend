from typing import List

from auth_backend.permission.models import (Permission)
from auth_backend.role.models import Role
from rest_framework import serializers, exceptions
from rest_framework.compat import MinLengthValidator, MaxLengthValidator
from rest_framework.validators import UniqueValidator

from .permission import FlatPermissionSerialzer

__all__ = (
    'FullRoleSerializer',
    'FlatRoleSerializer',
    'ShortRoleSerializer',
)


class FlatRoleListSerialzer(serializers.ListSerializer):
    """
    Преобразует список ID ролей в список моделей и обратно

    List[int] <-> List[Role]
    """

    def to_representation(self, m2m) -> str:
        return m2m.get_queryset().values_list('id', flat=True)

    def to_internal_value(self, role_ids: List[int]) -> List[Role]:
        if type(role_ids) is list and all(type(x) is int for x in role_ids):
            return list(Role.objects.filter(id__in=role_ids))
        else:
            return super().to_internal_value(role_ids)


class FlatRoleSerializer(serializers.Serializer):
    """
    Преобразует код роли в модель и обратно

    int <-> Role
    """
    def to_representation(self, instance: Role) -> int:
        return instance.id

    def to_internal_value(self, role_id: int) -> Role:
        if isinstance(role_id, int):
            try:
                return Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                raise exceptions.NotFound(code='roleNotFound')
        elif isinstance(role_id, dict):
            return super().to_internal_value(role_id)

    class Meta:
        list_serializer_class = FlatRoleListSerialzer
        model = Role


class ShortRoleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'code', 'name')
        model = Role


class FullRoleSerializer(serializers.ModelSerializer):
    permissions = FlatPermissionSerialzer(many=True)
    name = serializers.CharField(validators=[
        MinLengthValidator(5), MaxLengthValidator(200),
        UniqueValidator(Role.objects.all())
    ])

    def create(self, validated_data: dict) -> Role:
        role_perms = validated_data.pop('permissions', None)
        role = super().create(validated_data)
        return self._set_role_permissions(role, role_perms)

    def update(self, role: Role, validated_data: dict) -> Role:
        role_perms = validated_data.pop('permissions', None)
        role = super().update(role, validated_data)
        return self._set_role_permissions(role, role_perms)

    def _set_role_permissions(self, role: Role,
                              role_perms: List[Permission]) -> Role:
        if role_perms:
            role.permissions.set(role_perms)
        elif role_perms is not None:
            role.permissions.clear()
        return role

    class Meta:
        fields = ('id', 'code', 'name', 'permissions')
        model = Role
