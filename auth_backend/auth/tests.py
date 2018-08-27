from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

__all__ = ('TestAuthentication',)

refresh_token = None

class TestAuthentication(APITestCase):
    """
    Тест кейс на авторизацию пользователя с использованием JWT
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='username',
            password='password',
        )

    def test_success_authentication(self):
        global refresh_token

        response = self.client.post('/api/auth/token/', {
            "username": 'username',
            "password": 'password'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        payload = response.json()
        self.assertTrue('access' in payload and 'refresh' in payload)
        refresh_token = payload['refresh']

    def test_token_refresh(self):
        if refresh_token != None:
            response = self.client.post('/api/auth/token/refresh/', {
                "refresh": refresh_token,
            }, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)        
