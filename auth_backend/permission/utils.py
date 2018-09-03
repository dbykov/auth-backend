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
    __populated = False

    @classmethod
    def add_code(cls, code, name):
        cls.__permission_codes[code] = name

    @classmethod
    def codes(cls):
        cls.populate()

        return cls.__permission_codes.keys()

    @classmethod
    def name_by_code(cls, code):
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


class IsAuthor:
    """
    Проверка пользователя на авторство над указанным объектом
    """
    def has_permission(self, *args, **kwargs):
        return True

    def has_object_permission(self, request, viewset, obj):
        return obj.is_owned_by(request.user)
