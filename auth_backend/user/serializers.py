from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from auth_backend.user.helpers import send_resetpassword_email

UserModel = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = self._get_user()

    def validate_uidb64(self, value):
        if self._user is None:
            raise serializers.ValidationError("User not found")

        return value

    def validate_token(self, value):
        if not default_token_generator.check_token(self._user, value):
            raise serializers.ValidationError("Token is invalid")

        return value

    def validate_confirm_password(self, value):
        new_password = self.initial_data.get('new_password')
        if new_password != value:
            raise serializers.ValidationError("Password mismatch")

        password_validation.validate_password(value, self._user)

        return value

    def save(self, **kwargs):
        self._user.set_password(self.validated_data.get('new_password'))
        self._user.email_verified = True
        self._user.save()

        return self._user

    def _get_user(self):
        try:
            uid = urlsafe_base64_decode(
                self.initial_data.get('uidb64')).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist,
                ValidationError):
            user = None
        return user


class RequestResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for reset password request.
    """
    email = serializers.EmailField(required=True)

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)
        self._user = self._get_user()

    def validate_email(self, value):
        if not self._user:
            raise serializers.ValidationError('User not found')

        return value

    def _get_user(self):
        try:
            user = UserModel._default_manager.get(
                email=self.initial_data.get('email'))
        except UserModel.DoesNotExist:
            user = None

        return user

    def send(self):
        send_resetpassword_email(self.context.get("request"), self._user)
