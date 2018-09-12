from django.db import models

from auth_backend.base.mixins import DateMixin

# Максимальная длина кода разрешения
PERMISSION_CODE_LENGTH = 64


class Permission(DateMixin):
    """
    Модель разрешения, привязанного к роли
    """
    code = models.CharField(
        max_length=PERMISSION_CODE_LENGTH,
        unique=True,
        verbose_name='Код разрешения')
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование разрешения')

    def __str__(self):
        return f'{self.id}: {self.name} ({self.code})'

    class Meta:
        db_table = 'permissions'
        verbose_name = 'Разрешение роли'
        verbose_name_plural = 'Разрешения ролей'


def create_or_update_permissions():
    from .utils import PermissionRegistry
    code2perm = {perm.code: perm for perm in Permission.objects.all()}
    new_perms = []

    for code in PermissionRegistry.codes():
        perm = code2perm.get(code)
        name = PermissionRegistry.name_by_code(code)
        if perm and perm.name != name:
            perm.name = name
            perm.save()
        elif perm is None:
            new_perms.append(Permission(code=code, name=name))

    Permission.objects.bulk_create(new_perms)
