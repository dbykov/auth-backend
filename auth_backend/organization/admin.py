from django.contrib import admin

from auth_backend.organization.models import (
    OrganizationType, Organization)
from auth_backend.address.models import Address


@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ['author', 'name']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'type']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'type',
        'zipcode',
        'place',
        'street',
        'house_num',
        'housing',
        'flat',
    ]
