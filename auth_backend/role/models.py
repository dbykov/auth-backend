from django.db import models
from django.db.models import PROTECT

from auth_backend.base.mixins import (
    UserMixin, DateMixin, OrganizationMixin)


class Role(UserMixin, DateMixin):
    """
    Модель пользовательских ролей
    """
    code = models.CharField(
        max_length=16, unique=True,
        verbose_name='Код роли')
    name = models.CharField(
        max_length=128, verbose_name='Наименование роли')
    permissions = models.ManyToManyField(
        to='permission.RolePermission',
        verbose_name='Список разрешений')

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'roles'
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'


class OrganizationRole(DateMixin, OrganizationMixin):
    """
    Модель ролей в организациях
    """
    role = models.ForeignKey(
        to='Role',
        verbose_name='Ссылка на роль',
        on_delete=PROTECT, related_name='organizations')

    def __str__(self):
        return f'{self.id}: {self}'

    class Meta:
        db_table = 'organization_roles'
        verbose_name = 'Роль на учреждении'
        verbose_name_plural = 'Роли на учреждениях'
