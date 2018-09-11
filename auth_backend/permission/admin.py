from django.contrib import admin

from auth_backend.permission.models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    readonly_fields = ['code']
    ordering = ['name']
