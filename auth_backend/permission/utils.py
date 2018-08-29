"""
Базовая информация о разрешениях
"""

#
# Общие коды разрешений
# ========================================================================

# Разрешение на редактирование
PERM_EDIT = 'edit'
# Разрешение на просмотр (одного объекта или списка)
PERM_VIEW = 'view'
# Разрешение на удаление
PERM_DELETE = 'delete'
# Разрешение на добавление новой записи
PERM_ADD = 'add'

# Общий список базовых (CRUD) разрешений
BASE_PERMS = (PERM_EDIT, PERM_VIEW, PERM_DELETE, PERM_ADD)


class PermissionRegistry:
    """
    Регистр имеющихся в системе разрешений
    """
    __permission_codes = {}

    @classmethod
    def add_code(cls, code, name):
        cls.__permission_codes[code] = name

    @classmethod
    def codes(cls):
        return cls.__permission_codes.keys()

    @classmethod
    def name_by_code(cls, code):
        return cls.__permission_codes[code]
