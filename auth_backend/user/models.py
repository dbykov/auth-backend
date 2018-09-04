from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models

from auth_backend.user.enums import Gender


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя системы
    """
    email = models.EmailField(
        verbose_name='Эл.почта',
        unique=True)
    is_active = models.BooleanField(
        verbose_name='Активный',
        default=True)
    roles = models.ManyToManyField(
        to='role.OrganizationRole',
        verbose_name='Роли пользователя',
        blank=True)
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True)
    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices(),
        verbose_name='Пол', default=Gender.MALE)
    birth_date = models.DateField(
        verbose_name='Дата рождения', null=True)

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

    def __str__(self):
        username = getattr(self, self.USERNAME_FIELD, '')

        return f'{self.id}: {username}'

    class Meta:
        abstract = True
