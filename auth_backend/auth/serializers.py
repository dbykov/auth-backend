from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenObtainSerializer(TokenObtainPairSerializer):

    default_error_messages = {
        'no_active_account': _(
            'No active account found with the given credentials'),
        'inactive_account': _(
            'Account with the given credentials is inactive'),
    }

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        if not self.user.is_active:
            raise exceptions.PermissionDenied(
                self.error_messages['inactive_account'],
                'inactive_account',
            )

        data = {}

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
