from functools import wraps

from rest_framework.exceptions import PermissionDenied

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
    # Декорируемый метод
    callable = None
    # Класс-viewset
    viewset = None
    # Базовый код разрешения для данного конкретного метода
    permission_code = None
    # Человекопонятное наименование разрешения
    verbose_name = None
    # Признак, что указанный метод уже был декорирован
    is_wrapped = True

    def __init__(self, fn):
        self.callable = fn

        self.__doc__ = fn.__doc__
        self.__name__ = fn.__name__

    @property
    def full_code(self):
        """
        Полный код разрешения
        """
        return f'{self.viewset.name}:{self.permission_code}'

    def __call__(self, viewset, request):
        if not request.user.has_permission(self.full_code):
            raise PermissionDenied('Нет прав для доступа к ресурсу')

        return self.callable.__call__(viewset, request)


class WrappedLabel:
    """
    Обертка над кастомным методом-отображением
    Добавляет признак для последующей постобработки в рантайме
    """
    callable = None
    permission_code = None
    verbose_name = None
    is_wrapped = False

    def __init__(self, fn, perm_code, verbose_name):
        self.callable = fn
        self.permission_code = perm_code
        self.verbose_name = verbose_name

    def __call__(self, request):
        return self.callable(request)


def _wrap_method(cls, perm_code, method_name, verbose_name):
    """
    Оборачивание метода с указанным наименованием
    в указанном классе для добавления поддержки системы ролей

    :param cls: Класс, в котором будет выполнятся поиск метода (viewset)
    :param perm_code: Базовый код разрешения
    :param method_name: Имя искомого метода-отображения
    :param verbose_name: Человекопонятное наименование для права
    """
    def overrided_dispatch(self, request, *args, **kwargs):
        """
        Перекрытый метод dispatch из viewset
        Добавлена передача ссылки на viewset в вызываемый метод.
        Необходимость возникла в связи с тем,
        что вызываемый метод оборачивается в WrappedMethod
        и информация о родительском классе теряется
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(),
                    self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            # TODO: Добавлена передача ссылки на текущий класс (self)
            response = handler(self, request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(
            request, response, *args, **kwargs)

        return self.response

    # Переопределяем метод dispatch (возможно есть способ обойтись без этого?)
    cls.dispatch = overrided_dispatch

    existed_method = getattr(cls, method_name, None)
    if existed_method is not None:
        wrapped_method = WrappedMethod(existed_method)
        wrapped_method.viewset = cls
        wrapped_method.permission_code = perm_code
        wrapped_method.verbose_name = verbose_name

        setattr(cls, method_name, wrapped_method)

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
    # Проверка на наличие у viewset атрибута verbose_name.
    # Значение данного атрибута используется в качестве части
    # человекопонятного наименования разрешения.
    assert getattr(cls, 'verbose_name', None), (
        'Необходимо указать атрибут verbose_name!')

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
    for name in cls.__dict__.keys():
        obj = getattr(cls, name, None)
        if obj is not None and hasattr(obj, 'is_wrapped'):
            if obj.is_wrapped:
                continue

            _wrap_method(cls, obj.permission_code, name, obj.verbose_name)

    return cls


def permission_required(perm_code, verbose_name):
    """
    Добавление требования определенного кода разрешение для данного действия
    :param perm_code: Код разрешения
    """
    def outer(view):
        def inner(*args, **kwargs):
            return view(*args, **kwargs)

        return WrappedLabel(inner, perm_code, verbose_name)
    return outer

