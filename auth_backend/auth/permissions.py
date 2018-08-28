
PERM_EDIT = 'edit'
PERM_VIEW = 'view'
PERM_DELETE = 'delete'
PERM_ADD = 'add'

BASE_PERMS = (PERM_EDIT, PERM_VIEW, PERM_DELETE, PERM_ADD)


class PermissionRegistry:
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
