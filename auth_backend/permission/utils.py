"""
Базовая информация о разрешениях
"""
import logging
from typing import Iterator, KeysView, Dict

log = logging.getLogger(__name__)

#
# Общие коды разрешений
# ========================================================================

# Разрешение на редактирование
PERM_EDIT = 'edit'
PERM_EDIT_DEFAULT = (PERM_EDIT, 'Редактирование')

# Разрешение на просмотр (одного объекта или списка)
PERM_VIEW = 'view'
PERM_VIEW_DEFAULT = (PERM_VIEW, 'Просмотр')

# Разрешение на удаление
PERM_DELETE = 'delete'
PERM_DELETE_DEFAULT = (PERM_DELETE, 'Удаление')

# Разрешение на добавление новой записи
PERM_ADD = 'add'
PERM_ADD_DEFAULT = (PERM_ADD, 'Создание')


# Общий список базовых (CRUD) разрешений
BASE_PERMS = (PERM_EDIT, PERM_VIEW, PERM_DELETE, PERM_ADD)


class PermissionRegistry:
    """
    Регистр имеющихся в системе разрешений
    """
    __permission_codes: Dict[str, str] = {}
    __populated: bool = False

    @classmethod
    def add_code(cls, code: str, name: str):
        if code not in cls.__permission_codes:
            cls.__permission_codes[code] = name

    @classmethod
    def codes(cls) -> KeysView:
        cls.populate()

        return cls.__permission_codes.keys()

    @classmethod
    def all_codes_by_permission_code(cls, permission_code: str) -> Iterator:
        """
        Возвращает список всех кодов разрешений для указанного типа
        (например, PERM_VIEW)

        :param permission_code: Код разрешения
        """
        return filter(lambda x: x.split(':')[1] == permission_code, cls.codes())

    @classmethod
    def name_by_code(cls, code: str) -> str:
        return cls.__permission_codes[code]

    @classmethod
    def populate(cls):
        """
        Заполнение реестра, если он не заполнился ранее
        (например при запуске тестов)
        """
        if cls.__populated:
            return

        from django.conf import settings
        root_urls = settings.ROOT_URLCONF
        __import__(root_urls)

        cls.__populated = True


def create_or_update_permissions():
    from .models import Permission

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
