from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auth_backend.permission.views import RolePermissionViewSet
from auth_backend.role.views import RoleViewSet
from auth_backend.organization.views import (
    OrganizationViewSet, OrganizationTypeViewSet)
from auth_backend.user.views import UserViewSet


router = DefaultRouter()
# Пользователи
router.register('users', UserViewSet, base_name='user')
# Структурные единицы
router.register('organizations', OrganizationViewSet, base_name='organization')
# Типы структурных единиц
router.register('organization-types', OrganizationTypeViewSet, base_name='organization-type')  # noqa
# Список пользовательских ролей
router.register('roles', RoleViewSet, base_name='role')
# Список разрешений
router.register('permissions', RolePermissionViewSet, base_name='permission')


# Общие механизмы аутентификации
urlpatterns = [
    path('auth/', include('auth_backend.auth.urls')),
] + router.urls
