from auth_backend.permission.signals import after_create_permissions


def create_permissions(sender, *args, **kwargs):
    """
    Формирование отсутствующих разрешений ролей
    """
    from auth_backend.permission.apps import PermissionAppConfig
    from auth_backend.permission.models import MetaPermission
    from auth_backend.permission.utils import PermissionRegistry

    # Добавляем записи только при миграции основного модуля
    if not isinstance(sender, PermissionAppConfig):
        return

    print('Create permissions...')

    all_codes = set(PermissionRegistry.codes())
    existed_codes = set(MetaPermission.objects.filter(
        code__in=all_codes
    ).values_list('code', flat=True))

    non_existed_codes = all_codes - existed_codes
    for code in non_existed_codes:
        name = PermissionRegistry.name_by_code(code)
        MetaPermission.objects.create(
            code=code,
            name=name)

    print(f'Created {len(non_existed_codes)} permissions.')

    after_create_permissions.send(None)
