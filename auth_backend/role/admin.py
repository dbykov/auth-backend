from django.contrib import admin

from auth_backend.role.models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    filter_horizontal = ['permissions']