from auth_backend.auth.permissions import PermissionRegistry


def create_permissions(sender, *args, **kwargs):
    """
    Формирование отсутствующих разрешений ролей
    """
    from auth_backend.models import Permission

    all_codes = set(PermissionRegistry.codes())
    existed_codes = set(Permission.objects.filter(
        code__in=all_codes
    ).values_list('code', flat=True))

    non_existed_codes = all_codes - existed_codes
    for code in non_existed_codes:
        name = PermissionRegistry.name_by_code(code)
        Permission.objects.create(
            code=code,
            name=name,
        )
