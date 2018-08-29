from django.contrib import admin

from auth_backend.permission.models import MetaPermission, RolePermission


@admin.register(MetaPermission)
class MetaPermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'meta_permission']
    filter_horizontal = ['organizations']
    readonly_fields = ['code']