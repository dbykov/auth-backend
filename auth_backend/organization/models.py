from django.conf import settings
from django.db import models
from django.db.models import PROTECT
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from auth_backend.base.mixins import UserMixin, DateMixin


class OrganizationType(UserMixin, DateMixin):
    """
    Модель типа организации
    """
    name = models.CharField(
        max_length=64,
        verbose_name='Наименование типа организации')

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'organization_types'
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы организаций'


class Organization(UserMixin, DateMixin, MPTTModel):
    """
    Модель организации
    """
    full_name = models.TextField(
        verbose_name='Полное наименование организации', blank=True)
    short_name = models.CharField(
        max_length=128,
        verbose_name='Наименование организации')
    type = models.ForeignKey(
        to='OrganizationType',
        verbose_name='Тип организаций',
        on_delete=PROTECT)
    parent = TreeForeignKey(
        to='self', null=True,
        blank=True, related_name='children',
        on_delete=models.CASCADE,
        verbose_name='Ссылка на родительский узел')
    inn = models.CharField(
        max_length=12, verbose_name='ИНН',
        default='', blank=True)
    kpp = models.CharField(
        max_length=12, verbose_name='КПП',
        default='', blank=True)
    okato = models.CharField(
        max_length=12, verbose_name='ОКАТО',
        default='', blank=True)
    license = models.CharField(
        max_length=128, verbose_name='Номер лицензии',
        default='', blank=True)
    boss = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='Руководитель организации',
        related_name='boss_organizations',
        null=True, on_delete=PROTECT, blank=True)
    address_jur = models.ForeignKey(
        to='address.Address', verbose_name='Юридический адрес',
        null=True, on_delete=PROTECT,
        related_name='jur_organizations', blank=True)
    address_fact = models.ForeignKey(
        to='address.Address', verbose_name='Фактический адрес',
        null=True, on_delete=PROTECT,
        related_name='fact_organizations', blank=True)
    phone = models.CharField(
        max_length=32, verbose_name='Телефон',
        default='', blank=True)
    email = models.CharField(
        max_length=128, verbose_name='Эл.почта',
        default='', blank=True)
    site = models.CharField(
        max_length=128, verbose_name='Сайт',
        default='', blank=True)

    def __str__(self):
        return f'{self.id}: {self.short_name} ({self.type.name})'

    class Meta:
        db_table = 'organizations'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
