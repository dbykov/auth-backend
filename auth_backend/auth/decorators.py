from rest_framework.exceptions import PermissionDenied

from auth_backend.auth.permissions import (
    PERM_ADD, PERM_VIEW, PERM_EDIT,
    PERM_DELETE, PermissionRegistry)


class WrappedMethod:
    callable = None
    viewset = None
    permission_code = None
    verbose_name = None
    is_wrapped = True

    def __init__(self, fn):
        self.callable = fn

    @property
    def full_code(self):
        return f'{self.viewset.name}:{self.permission_code}'

    def __call__(self, viewset, request):
        if not request.user.has_permission(self.full_code):
            raise PermissionDenied('Нет прав для доступа к ресурсу')

        return self.callable.__call__(viewset, request)


class WrappedLabel:
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
    def overrided_dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(),
                    self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(self, request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(
            request, response, *args, **kwargs)

        return self.response

    cls.dispatch = overrided_dispatch

    existed_method = getattr(cls, method_name, None)
    if existed_method is not None:
        wrapped_method = WrappedMethod(existed_method)
        wrapped_method.viewset = cls
        wrapped_method.permission_code = perm_code
        wrapped_method.verbose_name = verbose_name

        setattr(cls, method_name, wrapped_method)

        PermissionRegistry.add_code(
            code=f'{cls.name}:{perm_code}',
            name=f'{cls.verbose_name}:{verbose_name}',
        )


def add_permissions(cls):
    assert cls.name is not None, (
        'Необходимо указать наименование отображения!')

    crud_perms = (
        (PERM_ADD, 'create', 'Создание'),
        (PERM_VIEW, ('retrieve', 'list'), 'Просмотр'),
        (PERM_EDIT, ('update', 'partial_update'), 'Редактирование'),
        (PERM_DELETE, 'destroy', 'Удаление'),
    )

    for code, method_name, verbose_name in crud_perms:
        if isinstance(method_name, (list, tuple)):
            for name in method_name:
                _wrap_method(cls, code, name, verbose_name)
        else:
            _wrap_method(cls, code, method_name, verbose_name)

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

