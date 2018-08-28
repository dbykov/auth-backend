from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


__all__ = ('TestUsersAsSuperUser', 'TestUsersAsRegularUser')


User = get_user_model()


class TestUsersAsSuperUser(APITestCase):
    """
    Тест кейс на работу со списком пользователей от лица админа
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
        
        jwt = self.client.post('/api/auth/token/', {
            'username': 'admin', 
            'password': 'admin'
        }).json()['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt}')

    def test_list_users(self):
        # when:
        response = self.client.get('/api/users/', format='json')
       
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = response.json()
        self.assertTrue(len(users) == 1)
        
        user = users[0]
        self.assertEqual(user['id'], self.superuser.id)
        self.assertEqual(user['username'], self.superuser.username)
        self.assertEqual(user['email'], self.superuser.email)
        self.assertEqual(user['is_active'], self.superuser.is_active)
        
    def test_add_user(self):
        # when:
        response = self.client.post('/api/users/', {
            "username": "user",
            "password": "user",
            "email": "user@example.com",
            "is_active": True
        }, format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_get_details(self):
        # setup:
        user = User.objects.create_user(
            username='user',
            password='user',
        )

        # when:
        response = self.client.get(f'/api/users/{user.id}/', format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_details = response.json()
        self.assertEqual(user_details['id'], user.id)

    def test_full_update_user(self):
        # setup:
        user = User.objects.create_user(**{
            "username": "user",
            "password": "user",
            "email": "user@example.com",
            "is_active": True
        })

        # when:
        response = self.client.put(f'/api/users/{user.id}/', {
            "username": "user2",
        }, format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_user(self):
        # setup:
        user = User.objects.create_user(
            username='user',
            password='user',
        )

        # when:
        response = self.client.patch(f'/api/users/{user.id}/', {
            "username": "user2",
        }, format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        # setup:
        user = User.objects.create_user(
            username='user',
            password='user',
        )

        # when:
        response = self.client.delete(f'/api/users/{user.id}/', format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestUsersAsRegularUser(APITestCase):
    """
    Тест кейс на работу со списком пользователей от лица обычного пользователя
    """

    def setUp(self):
        self.superuser = User.objects.create_user(
            username='regular',
            password='regular',
            email='regular@example.com'
        )
        
        jwt = self.client.post('/api/auth/token/', {
            'username': 'regular', 
            'password': 'regular'
        }).json()['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt}')

    def test_list_users(self):
        # when:
        response = self.client.get('/api/users/', format='json')
       
        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_user(self):
        # when:
        response = self.client.post('/api/users/', {
            "username": "user",
            "password": "user",
            "email": "user@email.com",
            "is_active": True
        }, format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_details(self):
        # when:
        response = self.client.get(f'/api/users/123/', format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_user(self):
        # when:
        response = self.client.put(f'/api/users/123/', {
            "username": "user2",
        }, format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_user(self):
        # when:
        response = self.client.patch(f'/api/users/123/', {
            "username": "user2",
        }, format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        # when:
        response = self.client.delete(f'/api/users/123/', format='json')

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
