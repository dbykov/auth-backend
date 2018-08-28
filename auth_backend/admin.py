from django.contrib import admin
from auth_backend.models import (
    StructureType, Structure, User, Role)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'is_active',
        'is_superuser',
    ]
    filter_horizontal = ['roles']


@admin.register(StructureType)
class StructureTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
