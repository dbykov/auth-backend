from auth_backend.permission.receivers import create_permissions
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PermissionAppConfig(AppConfig):
    name = 'auth_backend.permission'
    verbose_name = 'Разрешения'

    def ready(self):
        post_migrate.connect(create_permissions)
