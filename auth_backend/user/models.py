from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE, PROTECT

from auth_backend.user.enums import Gender


class UserMixin:
    """
    Добавляет в класс поле с ссылкой на автора (пользователя)
    """
    author = models.ForeignKey(
        to='User', null=True,
        verbose_name='Ссылка на пользователя',
        on_delete=CASCADE)


class User(AbstractUser):
    """
    Модель пользователя системы
    """
    roles = models.ManyToManyField(
        to='role.Role',
        verbose_name='Роли пользователя')
    first_name = models.CharField(
        max_length=30, verbose_name='Имя',
        default='', blank=True)
    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия',
        default='', blank=True)
    patronymic = models.CharField(
        max_length=150, verbose_name='Отчество',
        default='', blank=True)
    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices(),
        verbose_name='Пол', default=Gender.MALE)
    birth_date = models.DateField(
        verbose_name='Дата рождения', null=True)
    organization = models.ForeignKey(
        to='organization.Organization',
        verbose_name='Ссылка на организацию',
        null=True,
        on_delete=PROTECT, related_name='users')
    position = models.CharField(
        max_length=128, verbose_name='Должность',
        default='')
    photo = models.FileField(
        verbose_name='Фото',
        null=True, upload_to='photos/')
    admission_date = models.DateField(
        verbose_name='Дата приема на работу', null=True)
    phone = models.CharField(
        max_length=128, verbose_name='Телефон',
        default='', blank=True)
    address = models.ForeignKey(
        to='address.Address',
        verbose_name='Адрес', null=True,
        on_delete=PROTECT)

    def has_permission(self, code):
        """
        Проверка наличия указанного кода разрешения у указанного пользователя
        У суперадмина по умолчанию есть все возможные разрешения
        """
        result = self.is_superuser

        if not result:
            result = self.__class__.objects.filter(
                roles__permissions__code=code
            ).exists()

        return result

    @property
    def fio(self):
        """
        Полное ФИО
        """
        return ' '.join(filter(None, (
            self.first_name,
            self.last_name,
            self.patronymic,
        )))

    def __str__(self):
        return f'{self.id}: {self.username} ({self.fio})'

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь системы'
        verbose_name_plural = 'Пользователи системы'
