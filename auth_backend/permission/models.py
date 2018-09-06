from django.db import models
from django.db.models import PROTECT

from auth_backend.base.mixins import UserMixin, DateMixin

# Максимальная длина кода разрешения
PERMISSION_CODE_LENGTH = 64


class MetaPermission(DateMixin):
    """
    Модель базового разрешения
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
        db_table = 'meta_permissions'
        verbose_name = 'Базовое разрешение роли'
        verbose_name_plural = 'Базовые разрешения ролей'


class RolePermission(UserMixin, DateMixin):
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
    meta_permission = models.ForeignKey(
        to='MetaPermission',
        verbose_name='Ссылка на базовое разрешение',
        on_delete=PROTECT)

    def __str__(self):
        return f'{self.id}: {self.name} ({self.code})'

    def save(
            self, force_insert=False, force_update=False, using=None,
            update_fields=None):

        # Код разрешения всегда должен соответствовать коду базового разрешения
        self.code = self.meta_permission.code

        return super(RolePermission, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    class Meta:
        db_table = 'permissions'
        verbose_name = 'Разрешение роли'
        verbose_name_plural = 'Разрешения ролей'
