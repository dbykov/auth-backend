from rest_framework import permissions, viewsets
from rest_framework_simplejwt import authentication
from . import serializers, User


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
