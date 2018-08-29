from auth_backend.auth.decorators import add_permissions
from rest_framework import viewsets

from auth_backend.organization.models import (
    OrganizationType, Organization)
from auth_backend.organization.serializers import (
    OrganizationTypeSerializer, OrganizationSerializer)


@add_permissions
class OrganizationViewSet(viewsets.ModelViewSet):
    name = 'organization'
    verbose_name = 'Организация'
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


@add_permissions
class OrganizationTypeViewSet(viewsets.ModelViewSet):
    name = 'organization-type'
    verbose_name = 'Тип организации'
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer


