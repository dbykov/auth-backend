from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class PasswordRecovery(APITestCase):
    """
    Тест кейсы на восстановление пароля
    """
    def setUp(self):
        self._user = User.objects.create_user(
            email='username@example.com',
            password='password',
        )
        self._uidb64 = urlsafe_base64_encode(
            force_bytes(self._user.pk)).decode()

    def test_reset_password(self):
        """
        Кейс: сброс пароля => задание нового пароля => аутентификация
        """
        # Установка нового пароля
        response = self.client.put(f'/password/reset/', {
            'uidb64': self._uidb64,
            'token': self._make_token(),
            'new_password': 'new_password',
            'confirm_password': 'new_password',
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Аутентификация с новыми кредами должна пройти
        response = self.client.post('/token/', {
            "email": 'username@example.com',
            "password": 'new_password'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Аутентификация со старыми кредами не должна пройти
        response = self.client.post('/token/', {
            "email": 'username@example.com',
            "password": 'password'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_passwords_equality(self):
        # Новый пароль совпадает с подтверждением пароля
        response = self.client.put(f'/password/reset/', {
            'uidb64': self._uidb64,
            'token': self._make_token(),
            'new_password': 'new_password',
            'confirm_password': 'new_password',
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Новый пароль не совпадает с подтверждением пароля
        response = self.client.put(f'/password/reset/', {
            'uidb64': self._uidb64,
            'token': self._make_token(),
            'new_password': 'new_password',
            'confirm_password': 'confirm_password',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_validation(self):
        # Длина пароля должна быть не менее 10 символов
        response = self.client.put(f'/password/reset/', {
            'uidb64': self._uidb64,
            'token': self._make_token(),
            'new_password': 'long_password',
            'confirm_password': 'long_password',
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # пароль короче 10 символов
        response = self.client.put(f'/password/reset/', {
            'uidb64': self._uidb64,
            'token': self._make_token(),
            'new_password': 'pass',
            'confirm_password': 'pass',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Пароль может содержать латинские и кириллические буквы и цифры,
        # а также специальные символы.
        response = self.client.put(f'/password/reset/', {
            'uidb64': self._uidb64,
            'token': self._make_token(),
            'new_password': 'password содержит кириллицу и 123"№;%:?',
            'confirm_password': 'password содержит кириллицу и 123"№;%:?',
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Пароль не должен совпадать с e-mail.
        response = self.client.put(f'/password/reset/', {
            'uidb64': self._uidb64,
            'token': self._make_token(),
            'new_password': self._user.email,
            'confirm_password': self._user.email,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _make_token(self):
        # Токен генерируется на основе даты последнего входа юзера,
        # поэтому надо рефрешить объект юзера из бд
        self._user.refresh_from_db()

        return default_token_generator.make_token(self._user)
