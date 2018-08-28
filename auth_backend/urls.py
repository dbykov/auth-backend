from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auth_backend.auth.views import RoleViewSet
from auth_backend.structures.views import (
    StructureViewSet, StructureTypeViewSet)
from auth_backend.users.views import UserViewSet


router = DefaultRouter()
# Пользователи
router.register('users', UserViewSet, base_name='user')
# Структурные единицы
router.register('structures', StructureViewSet, base_name='structure')
# Типы структурных единиц
router.register('structure-types', StructureTypeViewSet, base_name='structure-type')  # noqa
# Список пользовательских ролей
router.register('roles', RoleViewSet, base_name='role')


# Общие механизмы аутентификации
urlpatterns = [
    path('auth/', include('auth_backend.auth.urls')),
] + router.urls
