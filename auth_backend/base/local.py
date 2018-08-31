from threading import local
from typing import Union


__all__ = (
    'get_thread_data',
    'get_thread_session_data',
    'set_thread_session_data',
)


_thread_local = local()


class ThreadLocalData:
    """
    Данные текущего потока
    """
    # Идентификатор пользователя
    user_id: Union[int, None] = None
    # Дополнительные пользовательские данные
    __session_data: dict = {}

    def reset(self):
        """
        Сброс данных
        """
        self.user_id = None
        self.__session_data = {}

    def get(self, key, default=None):
        return self.__session_data.get(key, default)

    def set(self, key, value):
        self.__session_data[key] = value

    def delete(self, key):
        del self.__session_data[key]

    def has(self, key):
        return key in self.__session_data

    def flush_session_data(self):
        self.__session_data = {}


def get_thread_data():
    """
    Получение объекта с данными по контексту текущего запроса
    """
    if not hasattr(_thread_local, 'data'):
        _thread_local.data = ThreadLocalData()

    return _thread_local.data


def set_thread_session_data(key, value):
    """
    Добавление в контекст запроса пользовательских данных
    """
    _thread_local.data.set(key, value)


def get_thread_session_data(key, default=None):
    """
    Поиск в контексте запроса пользовательских данных
    """
    return _thread_local.data.get(key, default)
