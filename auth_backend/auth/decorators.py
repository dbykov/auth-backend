from typing import Type

from django.db.models import Q
from rest_framework.viewsets import ViewSetMixin

from auth_backend.permission.models import Permission
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
    namespace = None
    # Базовый код разрешения для данного конкретного метода
    permission_code = None
    # Человекопонятное наименование разрешения
    verbose_name = None
    # Признак, что указанный метод уже был декорирован
    is_wrapped = True
    # Признак того, что метод является публичным и права проверять не нужно
    is_public = False

    def __init__(self, namespace, permission_code, verbose_name, is_public):
        self.namespace = namespace
        self.permission_code = permission_code
        self.verbose_name = verbose_name
        self.is_public = is_public

    def full_code(self, namespace):
        """
        Полный код разрешения
        """
        return f'{namespace}:{self.permission_code}'

    @property
    def permissions(self):
        qfilter = Permission.objects.none()

        if isinstance(self.namespace, str):
            qfilter = Q(code=self.full_code(self.namespace))
        elif isinstance(self.namespace, (list, tuple)):
            qfilter = Q()
            for space in self.namespace:
                qfilter |= Q(code=self.full_code(space))

        return Permission.objects.filter(qfilter)


def _wrap_method(cls, namespace, resource_name,
                 perm_code, method_name, verbose_name, is_public=False):
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
            namespace=namespace,
            permission_code=perm_code,
            verbose_name=verbose_name,
            is_public=is_public)

        if not hasattr(cls, '_wrappers'):
            cls._wrappers = {}

        cls._wrappers[method_name] = wrapped_method

        if resource_name and isinstance(namespace, str):
            # Добавляем код и наименования разрешения в общий регистр,
            # чтобы при миграциях можно было создать недостающие записи
            PermissionRegistry.add_code(
                code=f'{namespace}:{perm_code}',
                name=f'{resource_name}:{verbose_name}',
            )


def add_permissions(namespace, resource_name=None, extra_actions=None,
                    public_methods=None):
    """
    Обертка над классом-viewset
    Ищет базовый список методов по CRUD, добавляет каждому проверку прав
    """
    public_methods = public_methods or ()

    def wrapper(cls: Type):
        assert namespace is not None, (
            f'Необходимо передать namespace в '
            f'add_permissions для {cls.__name__}!')

        if issubclass(cls, ViewSetMixin):
            crud_perms = (
                (PERM_VIEW, 'list', 'Просмотр'),
                (PERM_VIEW, 'retrieve', 'Просмотр'),
                (PERM_ADD, 'create', 'Создание'),
                (PERM_EDIT, 'update', 'Редактирование'),
                (PERM_EDIT, 'partial_update', 'Редактирование'),
                (PERM_DELETE, 'destroy', 'Удаление'),
            )
        else:
            crud_perms = (
                (PERM_VIEW, 'get', 'Просмотр'),
                (PERM_ADD, 'post', 'Создание'),
                (PERM_EDIT, 'put', 'Редактирование'),
                (PERM_EDIT, 'patch', 'Редактирование'),
                (PERM_DELETE, 'delete', 'Удаление'),
            )

        # Обработка базовых методов-отображений
        for code, method_names, verbose_name in crud_perms:
            _wrap_method(cls, namespace, resource_name,
                         code, method_names, verbose_name,
                         is_public=method_names in public_methods)

        if extra_actions:
            assert isinstance(extra_actions, dict), (
                'extra_actions must be dict')

            for action, (code, verbose_name) in extra_actions.items():
                _wrap_method(cls, namespace, resource_name,
                             code, action, verbose_name,
                             is_public=action in public_methods)

        return cls

    return wrapper
