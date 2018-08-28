from rest_framework import serializers

from auth_backend.users import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_superuser',
        )
        model = User
