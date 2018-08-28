from rest_framework import viewsets

from auth_backend.models import Structure, StructureType
from auth_backend.structures.serializers import (
    StructireTypeSerializer, StructureSerializer)


class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer


class StructureTypeViewSet(viewsets.ModelViewSet):
    queryset = StructureType.objects.all()
    serializer_class = StructireTypeSerializer
