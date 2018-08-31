from django.db import models
from django.db.models import CASCADE, PROTECT

from auth_backend.base.managers import ByOrganizationManager


class UserMixin(models.Model):
    """
    Добавляет в класс поле с ссылкой на автора (пользователя)
    """
    author = models.ForeignKey(
        to='user.User', null=True,
        verbose_name='Автор',
        on_delete=CASCADE)

    class Meta:
        abstract = True


class DateMixin(models.Model):
    """
    Добавляет в класс поля с датой создания и изменения записи
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания записи')
    changed_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения записи')

    class Meta:
        abstract = True


class OrganizationMixin(models.Model):
    """
    Примесь, добавляющая ссылку на учреждение в модель
    Также добавляется менеджер, который добавляет фильтр только
    по текущему активному учреждению.
    """
    organization = models.ForeignKey(
        to='organization.Organization',
        verbose_name='Ссылка на организацию',
        on_delete=PROTECT)

    objects = ByOrganizationManager()

    class Meta:
        abstract = True
