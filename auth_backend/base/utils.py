from django.core.cache import cache

from auth_backend.base.local import get_thread_data


# Префикс для ключа кэша,
# хранящего идентификатор текущей активной организации
ACTIVE_ORGANIZATION_PREFIX = 'active_organization'


def get_current_user_id():
    """
    Получение идентификатора текущего активного пользователя
    """
    return get_thread_data().user_id


def get_current_user(raise_exc=False):
    """
    Получение объекта текущего активного пользователя

    :param raise_exc: Необходимо ли выбрасывать исключение,
        если пользователь не найдет
    """
    from auth_backend.user.models import User

    result = None
    try:
        result = User.objects.get(pk=get_current_user_id())
    except User.DoesNotExist:
        if raise_exc:
            raise

    return result


def get_active_organization_id():
    """
    Получение идентификатора текущей активной организации
    """
    key = f'{ACTIVE_ORGANIZATION_PREFIX}::{get_current_user_id()}'

    return cache.get(key)


def set_active_organization(organization_id):
    """
    Установка текущей активной организации текущего активного пользователя
    """
    key = f'{ACTIVE_ORGANIZATION_PREFIX}::{get_current_user_id()}'
    cache.set(key, organization_id)
