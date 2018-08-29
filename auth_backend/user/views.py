from auth_backend.auth.decorators import add_permissions
from rest_framework import viewsets
from rest_framework_simplejwt import authentication

from auth_backend.user.models import User
from . import serializers


@add_permissions
class UserViewSet(viewsets.ModelViewSet):
    name = 'user'
    verbose_name = 'Пользователь'
    authentication_classes = (authentication.JWTAuthentication,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
