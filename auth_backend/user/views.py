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
    Установка нового пароля
    """
    permission_classes = (AllowAny,)

    def put(self, request, *args, **kwargs):
        """
        Изменение пароля
        """
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestResetPasswordView(APIView):
    """
    Запрос на сброс пароля
    """
    permission_classes = (AllowAny,)
    throttle_classes = (ResetPasswordRateThrottle,)

    def post(self, request, *args, **kwargs):
        serializer = RequestResetPasswordSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.send()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
