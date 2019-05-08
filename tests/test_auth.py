from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

__all__ = ('TestAuthentication',)

User = get_user_model()


class TestAuthentication(APITestCase):
    """
    Тест кейс на авторизацию пользователя с использованием JWT
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email='username@example.com',
            password='password',
        )

    def test_success_authentication_and_refresh_token(self):
        # when: пользователь указывает корректные креды
        response = self._auth_user()
        # then: пользователь авторизован
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # and: ответ содержит оба токена
        payload = response.data
        self.assertTrue('access' in payload and 'refresh' in payload)

        # when: пользователь рефрешит токен
        response = self.client.post('/token/refresh/', {
            "refresh": payload['refresh'],
        }, format='json')
        # then: токен успешно обновлен
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_authentication(self):
        # when: пользователь указывает некорректные креды
        response = self.client.post('/token/', {
            "email": 'username@example.com',
            "password": 'wrong_password'
        }, format='json')
        # then: пользователь не авторизован
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        # setup:
        tokens = self._auth_user().data
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        # when: пользователь заносит refresh токен в черный список
        response = self.client.post(
            '/token/blacklist/', tokens, format='json')
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # and: пользователь больше не авторизован
        self.assertEqual(
            self.client.post(
                '/token/refresh/', tokens, format='json').status_code,
            status.HTTP_401_UNAUTHORIZED)

    def test_last_login_changed(self):
        # when: The User was created, but never logged in
        user = User.objects.get(email='username@example.com')
        # then:
        self.assertIsNone(user.last_login)

        # when:
        self._auth_user()
        # then:
        user.refresh_from_db()
        self.assertIsNotNone(user.last_login)

    def test_inactive_user(self):
        # setup:
        self.user.is_active = False
        self.user.save()

        # when:
        response = self._auth_user()

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"].code, "inactive_account")

    def _auth_user(self) -> Response:
        return self.client.post('/token/', {
            "email": 'username@example.com',
            "password": 'password'
        }, format='json')
