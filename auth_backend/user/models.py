from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models

from auth_backend.user.enums import Gender


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя системы
    """
    # Необходимо перекрыть в дочерних моделях
    roles = None

    email = models.EmailField(
        verbose_name='Эл.почта',
        unique=True)
    is_active = models.BooleanField(
        verbose_name='Активный',
        default=True)
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
        raise NotImplementedError

    def __str__(self):
        username = getattr(self, self.USERNAME_FIELD, '')

        return f'{self.id}: {username}'

    class Meta:
        abstract = True
