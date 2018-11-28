from .utils import create_or_update_administrator_role, \
    create_or_update_guest_role


def init_default_roles(*args, **kwargs):
    """
    Инициализирует системные роли: Гость и Администратор
    """
    create_or_update_guest_role()
    create_or_update_administrator_role()
