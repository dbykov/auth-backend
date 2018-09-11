from django.db import models

from auth_backend.base.mixins import DateMixin


class Role(DateMixin):
    """
    Модель пользовательских ролей
    """
    code = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Код роли')
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование роли')
    permissions = models.ManyToManyField(
        to='permission.Permission',
        verbose_name='Список разрешений')

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'roles'
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
