from django.contrib import admin

from auth_backend.role.models import Role, OrganizationRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    filter_horizontal = ['permissions']


@admin.register(OrganizationRole)
class OrganizationRoleAdmin(admin.ModelAdmin):
    list_display = ['role', 'organization']
