from auth_backend.receivers import create_permissions
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthBackendConfig(AppConfig):
    name = 'auth_backend'
    verbose_name = 'Аутентификация'

    def ready(self):
        # Создаем разрешения ролей после завершения миграций
        post_migrate.connect(create_permissions)
