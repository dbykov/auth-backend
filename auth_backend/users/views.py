from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets
from rest_framework_simplejwt import authentication
from django.contrib.auth import get_user_model
from . import serializers


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    list:
    Отображение всех пользователей в системе

    * Требуются права администратора

    create:
    Добавление пользователя
    
    * Требуются права администратора

    retrieve:
    Отображение информации о пользователе 
    
    * Требуются права администратора

    update:
    Изменение информации о пользователе

    * Требуются права администратора

    partial_update:
    Частичное изменение информации о пользователе

    * Требуются права администратора

    destroy:
    Удаление пользователя
    
    * Требуются права администратора
    """
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
