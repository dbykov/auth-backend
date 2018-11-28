from typing import List

from auth_backend.permission.models import Permission
from rest_framework import serializers

__all__ = (
    'FlatPermissionSerialzer',
)


class FlatPermissionListSerialzer(serializers.ListSerializer):
    """
    Преобразует список кодов пермишенов в список моделей и обратно

    List[str] <-> List[Permission]
    """

    def to_representation(self, m2m) -> str:
        return m2m.get_queryset().values_list('code', flat=True)

    def to_internal_value(self, perm_codes: List[str]) -> List[Permission]:
        known_codes = list(Permission.objects.filter(
            code__in=perm_codes).values_list('code', flat=True))
        unknown_codes = [code for code in perm_codes
                         if code not in known_codes]

        if unknown_codes:
            raise serializers.ValidationError(code='invalidCodes')

        return list(Permission.objects.filter(code__in=perm_codes))


class FlatPermissionSerialzer(serializers.Serializer):
    """
    Преобразует код пермишена в модель и обратно

    str <-> Permission
    """

    def to_representation(self, instance: Permission) -> str:
        return instance.code

    def to_internal_value(self, perm_code: str) -> Permission:
        return Permission.objects.get(code=perm_code)

    class Meta:
        list_serializer_class = FlatPermissionListSerialzer
