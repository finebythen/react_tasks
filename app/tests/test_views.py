from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import MainTask


USER = get_user_model()
URL_VERIFICATION = reverse('token_obtain_pair')


class TestCaseBase(APITestCase):
    def setUp(self):
        self.email = 'johndoe@email.com'
        self.password = 'johndoepassword'
        self.data = {
            'email': self.email,
            'password': self.password
        }
        USER.objects.create_user(email=self.email, password=self.password)

    @property
    def jwt_token(self):
        response = self.client.post(URL_VERIFICATION, self.data, format='json')
        token = response.data['access']
        return {"HTTP_AUTHORIZATION": f"JWT {token}"}


class UserAuthTest(TestCaseBase):
    def test_auth_user(self):
        response = self.client.post(URL_VERIFICATION, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)


class MaintaskListTest(TestCaseBase):
    url = reverse('maintask-list')

    def test_get_obj(self):
        self.client.credentials(**self.jwt_token)
        
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_obj(self):
        self.client.credentials(**self.jwt_token)
        user = USER.objects.get(email='johndoe@email.com')

        data = {
            'id': 1,
            'active': True,
            'slug': 'maintask-042',
            'created_by': user.id,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'title': 'Maintask #042'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubtaskListTest(TestCaseBase):
    url = reverse('subtask-list')

    def test_get_obj(self):
        self.client.credentials(**self.jwt_token)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_obj(self):
        self.client.credentials(**self.jwt_token)
        user = USER.objects.get(email='johndoe@email.com')

        maintask = MainTask.objects.create(
            id=2,
            active=True,
            slug='maintask-111',
            created_by=user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            title='Maintask #111'
        )

        data = {
            'id': 1,
            'active': True,
            'slug': 'subtask-001',
            'created_by': user.id,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'maintask': maintask.id,
            'title': 'Subtask #001'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)