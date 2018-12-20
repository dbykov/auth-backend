from typing import List, Iterable

from auth_backend.permission.models import Permission
from auth_backend.permission.utils import PermissionRegistry
from auth_backend.role.models import Role

__all__ = (
    'get_guest_role',
    'get_administrator_role',
    'create_or_update_administrator_role',
    'create_or_update_guest_role',
    'iter_permissions',

    'GUEST_ROLE_CODE',
    'ADMINISTRATOR_ROLE_CODE',
    'READONLY_ROLE_CODES',

)


GUEST_ROLE_CODE = 'guest'
GUEST_ROLE_NAME = 'Гость'

ADMINISTRATOR_ROLE_CODE = 'administrator'
ADMINISTRATOR_ROLE_NAME = 'Администратор'

READONLY_ROLE_CODES = (GUEST_ROLE_CODE, ADMINISTRATOR_ROLE_CODE)


def get_guest_role() -> Role:
    return Role.objects.filter(code=GUEST_ROLE_CODE).get()


def get_administrator_role() -> Role:
    return Role.objects.get(code=ADMINISTRATOR_ROLE_CODE)


def create_or_update_guest_role() -> Role:
    """
    Создает или обновляет роль "Гость"
    (по-умолчанию используется для всех пользователей без роли)
    """
    role = _create_or_update_role(code=GUEST_ROLE_CODE,
                                  name=GUEST_ROLE_NAME)
    role.permissions.set([])
    return role


def create_or_update_administrator_role() -> Role:
    """
    Создает или обновляет роль "Администратор"
    """
    role = _create_or_update_role(code=ADMINISTRATOR_ROLE_CODE,
                                  name=ADMINISTRATOR_ROLE_NAME)
    role.permissions.set(iter_permissions())
    return role


def _create_or_update_role(*, code, name) -> Role:
    role = Role.objects.filter(code=code).first() or Role.objects.create(
        code=code, name=name)
    role.name = name
    return role


def iter_permissions(codes: List[str] = None) -> Iterable[Role]:
    if codes is None:
        codes = PermissionRegistry.codes()
    return iter(Permission.objects.filter(code__in=codes))
