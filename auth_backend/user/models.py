import os

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import PROTECT

from auth_backend.base.utils import get_active_organization_id
from auth_backend.user.enums import Gender


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя системы
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True)
    email = models.EmailField('Эл.почта', blank=True)
    is_staff = models.BooleanField(
        'Статус персонала', default=False)
    is_superuser = models.BooleanField(
        'Суперадмин', default=False)
    is_active = models.BooleanField(
        'Активный', default=True)
    roles = models.ManyToManyField(
        to='role.OrganizationRole',
        verbose_name='Роли пользователя',
        blank=True)
    iname = models.CharField(
        max_length=30, verbose_name='Имя',
        default='', blank=True)
    fname = models.CharField(
        max_length=150, verbose_name='Фамилия',
        default='', blank=True)
    oname = models.CharField(
        max_length=150, verbose_name='Отчество',
        default='', blank=True)
    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices(),
        verbose_name='Пол', default=Gender.MALE)
    birth_date = models.DateField(
        verbose_name='Дата рождения', null=True)
    photo = models.FileField(
        verbose_name='Фото',
        null=True,
        upload_to=os.path.join(settings.MEDIA_ROOT, 'avatars'))
    admission_date = models.DateField(
        verbose_name='Дата приема на работу', null=True)
    phone = models.CharField(
        max_length=128, verbose_name='Телефон',
        default='', blank=True)
    address = models.ForeignKey(
        to='address.Address',
        verbose_name='Адрес', null=True,
        on_delete=PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def clean(self):
        super().clean()

        self.email = self.__class__.objects.normalize_email(self.email)

    def has_permission(self, code):
        """
        Проверка наличия указанного кода разрешения у указанного пользователя
        У суперадмина по умолчанию есть все возможные разрешения
        """
        result = self.is_superuser

        if not result:
            result = self.__class__.objects.filter(
                roles__role__permissions__code=code
            ).exists()

        return result

    def organizations(self):
        """
        Список идентификаторов организаций пользователя
        """
        return self.roles.values_list('organization', flat=True)

    def organization_positions(self):
        current_organization = get_active_organization_id()

        return self.roles.filter(
            organization=current_organization)

    @property
    def fio(self):
        """
        Полное ФИО
        """
        return ' '.join(filter(None, (
            self.fname,
            self.iname,
            self.oname,
        )))

    def __str__(self):
        return f'{self.id}: {self.username} {self.fio}'

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь системы'
        verbose_name_plural = 'Пользователи системы'
