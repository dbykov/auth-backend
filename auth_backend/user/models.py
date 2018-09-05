from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from auth_backend.user.enums import Gender


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Модель пользователя системы
    """
    # Необходимо перекрыть в дочерних моделях
    roles = None

    is_superuser = models.BooleanField(
        verbose_name='Superuser status',
        default=False)

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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
