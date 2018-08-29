from django.contrib import admin

from auth_backend.user.models import User


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
