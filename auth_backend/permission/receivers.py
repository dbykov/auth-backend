from auth_backend.permission.signals import after_create_permissions


def create_permissions(sender, *args, **kwargs):
    """
    Формирование и обновление разрешений ролей
    """
    from auth_backend.permission.apps import PermissionAppConfig
    from auth_backend.permission.models import create_or_update_permissions
    from auth_backend.permission.utils import PermissionRegistry

    # Добавляем записи только при миграции основного модуля
    if not isinstance(sender, PermissionAppConfig):
        return

    print('Create permissions...')
    create_or_update_permissions()

    after_create_permissions.send(None)
