from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from auth_backend.user.serializers import ChangePasswordSerializer, \
    RequestResetPasswordSerializer


class ResetPasswordRateThrottle(UserRateThrottle):
    rate = '1/min'


class ResetPasswordView(APIView):
    """
    Сброс и установка нового пароля
    """
    throttle_classes = (ResetPasswordRateThrottle,)
    permission_classes = (AllowAny,)

    def put(self, request, *args, **kwargs):
        """
        Изменение пароля
        """
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """
        Запрос на сброс пароля
        """
        serializer = RequestResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
