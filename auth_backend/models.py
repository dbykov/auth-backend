from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import PROTECT
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class User(AbstractUser):
    """
    Модель пользователя системы
    """
    roles = models.ManyToManyField(
        to='Role',
        verbose_name='Роли пользователя')

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь системы'
        verbose_name_plural = 'Пользователи системы'


class StructureType(models.Model):
    """
    Модель типа структурной единицы
    """
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование типа структурной единицы')

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'structure_types'
        verbose_name = 'Тип структурной единицы'
        verbose_name_plural = 'Типы структурных единиц'


class Structure(MPTTModel):
    """
    Модель структурной единицы
    """
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование структурной единицы')
    type = models.ForeignKey(
        to='StructureType',
        verbose_name='Тип структурной единицы',
        on_delete=PROTECT)
    parent = TreeForeignKey(
        to='self', null=True,
        blank=True, related_name='children',
        on_delete=models.CASCADE,
        verbose_name='Ссылка на родительский узел')

    def __str__(self):
        return f'{self.id}: {self.name} ({self.type.name})'

    class Meta:
        db_table = 'structures'
        verbose_name = 'Структурная единица'
        verbose_name_plural = 'Структурные единицы'


class Role(models.Model):
    """
    Модель пользовательских ролей
    """
    code = models.CharField(max_length=128, verbose_name='Код роли')
    name = models.CharField(max_length=128, verbose_name='Наименование роли')

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'roles'
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
