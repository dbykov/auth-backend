from django.contrib import admin

from auth_backend.permission.models import MetaPermission, RolePermission


@admin.register(MetaPermission)
class MetaPermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    ordering = ['name']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'meta_permission']
    readonly_fields = ['code']
    ordering = ['name']
