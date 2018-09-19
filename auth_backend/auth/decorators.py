from typing import Type, List, Callable

from auth_backend.permission.utils import (
    PERM_ADD, PERM_VIEW, PERM_EDIT,
    PERM_DELETE, PermissionRegistry)


class WrappedMethod:
    """
    Обертка для методов-экшенов в viewset
    Сохраняет некоторую мета-информацию о методе и viewset,
    а также человекопонятное наименование роли и действия,
    а также кода разрешения.
    Добавляет при вызове обернутого метода проверку на наличие прав
    """
    name = None
    # Базовый код разрешения для данного конкретного метода
    permission_code = None
    # Человекопонятное наименование разрешения
    verbose_name = None
    # Признак, что указанный метод уже был декорирован
    is_wrapped = True

    def __init__(self, viewset_name, permission_code, verbose_name):
        self.name = viewset_name
        self.permission_code = permission_code
        self.verbose_name = verbose_name

    @property
    def full_code(self):
        """
        Полный код разрешения
        """
        return f'{self.name}:{self.permission_code}'


def _wrap_method(cls, perm_code, method_name, verbose_name):
    """
    Оборачивание метода с указанным наименованием
    в указанном классе для добавления поддержки системы ролей

    :param cls: Класс, в котором будет выполнятся поиск метода (viewset)
    :param perm_code: Базовый код разрешения
    :param method_name: Имя искомого метода-отображения
    :param verbose_name: Человекопонятное наименование для права
    """
    existed_method = getattr(cls, method_name, None)
    if existed_method is not None:
        wrapped_method = WrappedMethod(
            viewset_name=cls.name,
            permission_code=perm_code,
            verbose_name=verbose_name)

        if not hasattr(cls, '_wrappers'):
            cls._wrappers = {}

        cls._wrappers[method_name] = wrapped_method

        if hasattr(cls, 'verbose_name'):
            # Если в самом методе отсутствует документирование,
            # то проставляем ему по наименованию права
            if not existed_method.__doc__:
                def _wrapper(*args, **kwargs):
                    return existed_method(*args, **kwargs)

                _wrapper.__doc__ = f'{cls.verbose_name}:{verbose_name}'
                _wrapper.__name__ = existed_method.__name__

                setattr(cls, method_name, _wrapper)

            # Добавляем код и наименования разрешения в общий регистр,
            # чтобы при миграциях можно было создать недостающие записи
            PermissionRegistry.add_code(
                code=f'{cls.name}:{perm_code}',
                name=f'{cls.verbose_name}:{verbose_name}',
            )


def add_permissions(cls):
    """
    Обертка над классом-viewset
    Ищет базовый список методов по CRUD, добавляет каждому проверку прав
    Также ищет помеченные декоратором permission_required
    и добавляет поддержку прав.
    """
    # Проверка на наличие у viewset атрибутa name.
    # Значение данного атрибута используется в качестве префикса
    # к полному коду разрешения.
    assert getattr(cls, 'name', None) is not None, (
        'Необходимо указать атрибут name!')

    if not getattr(cls, 'skip_crud_methods', False):
        crud_perms = (
            (PERM_ADD, 'create', 'Создание'),
            (PERM_VIEW, ('retrieve', 'list'), 'Просмотр'),
            (PERM_EDIT, ('update', 'partial_update'), 'Редактирование'),
            (PERM_DELETE, 'destroy', 'Удаление'),
        )

        # Обработка базовых методов-отображений
        for code, method_name, verbose_name in crud_perms:
            if isinstance(method_name, (list, tuple)):
                for name in method_name:
                    _wrap_method(cls, code, name, verbose_name)
            else:
                _wrap_method(cls, code, method_name, verbose_name)

    # Обработка кастомных методов-отображений,
    # помеченных декоратором permission_required
    keys = list(cls.__dict__.keys())
    for key in keys:
        if key.startswith('__'):
            continue

        obj = getattr(cls, key, None)
        is_wrapped = getattr(obj, 'is_wrapped', None)

        if obj is not None and is_wrapped is not None and not is_wrapped:
            _wrap_method(cls, obj.permission_code, key,
                         getattr(obj, 'verbose_name', None))

    return cls


def extend_permission_classes(*permission_classes: List[Type[object]]):
    """
    Расширяем список классов с проверкой разрешений
    """
    def wrapper(cls):
        cls.permission_classes = (
            cls.permission_classes + list(permission_classes))

        return cls
    return wrapper


def permission_required(perm_code: str, verbose_name: str) -> Callable:
    """
    Добавление требования определенного кода разрешение для данного действия

    :param perm_code: Код разрешения
    :param verbose_name: Наименование разрешения
    """
    def outer(view):
        view.permission_code = perm_code
        view.verbose_name = verbose_name
        view.is_wrapped = False

        return view
    return outer
