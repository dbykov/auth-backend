from rest_framework import viewsets

from auth_backend.address.models import Address
from auth_backend.address.serializers import AddressSerializer
from auth_backend.auth.decorators import add_permissions


@add_permissions
class AddressViewSet(viewsets.ModelViewSet):
    name = 'address'
    verbose_name = 'Адрес'
    queryset = Address.objects.all()
    serializer_class = AddressSerializer