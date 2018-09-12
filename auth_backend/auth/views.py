from django.contrib.auth import user_logged_in
from rest_framework import permissions, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RefreshTokenSerializer


class RefreshTokenBlacklistView(views.APIView):
    """
    Инвалидирует Refresh токен путем занесения в черный список
    """
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer = RefreshTokenSerializer()

    def post(self, request: Request, format=None) -> Response:
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']

        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            raise ValidationError('Invalid refresh token')

        return Response(status=status.HTTP_200_OK)

    # Для генерации документации
    def get_serializer(self) -> RefreshTokenSerializer:
        return self.serializer


class TokenObtainView(TokenObtainPairView):
    """
    Получение пары access и refresh токенов
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user_logged_in.send(
            sender=serializer.user.__class__, request=request,
            user=serializer.user)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
