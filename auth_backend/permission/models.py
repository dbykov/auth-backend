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


