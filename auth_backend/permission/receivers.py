from auth_backend.permission.signals import after_create_permissions


def create_permissions(sender, *args, **kwargs):
    """
    Формирование отсутствующих разрешений ролей
    """
    from auth_backend.permission.apps import PermissionAppConfig
    from auth_backend.permission.models import Permission
    from auth_backend.permission.utils import PermissionRegistry

    # Добавляем записи только при миграции основного модуля
    if not isinstance(sender, PermissionAppConfig):
        return

    print('Create permissions...')

    code2perm = {perm.code: perm for perm in Permission.objects.all()}
    new_perms = []

    for code in PermissionRegistry.codes():
        perm = code2perm.get(code)
        name = PermissionRegistry.name_by_code(code)
        if perm and perm.name != name:
            perm.name = name
            perm.save()
        elif perm is None:
            new_perms.append(Permission(code=code, name=name))

    Permission.objects.bulk_create(new_perms)
    print(f'Created {len(new_perms)} permissions.')

    after_create_permissions.send(None)
