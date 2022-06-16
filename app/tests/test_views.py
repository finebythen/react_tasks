import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import MainTask, SubTask


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
        self.user = USER.objects.get(email='johndoe@email.com')

        self.maintask = MainTask.objects.create(
            id=1,
            active=True,
            slug='maintask-42',
            created_by=self.user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            title='Maintask #42'
        )

        self.subtask = SubTask.objects.create(
            id=1,
            active=True,
            slug='subtask-42',
            created_by=self.user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            maintask=self.maintask,
            title='Subtask #42'
        )

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
            'id': 2,
            'active': True,
            'slug': 'maintask-142',
            'created_by': user.id,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'title': 'Maintask #142'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MaintaskDetailTest(TestCaseBase):
    url = reverse('maintask-detail', args=['maintask-42'])

    def test_obj_get(self):
        self.client.credentials(**self.jwt_token)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_obj_patch(self):
        self.client.credentials(**self.jwt_token)
        response = self.client.patch(self.url, kwargs={'active': False}, format='json')
        response_data = json.loads(response.content)
        task = MainTask.objects.get(slug='maintask-42')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('active'), task.active)

    
    def test_obj_delete(self):
        self.client.credentials(**self.jwt_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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

        data = {
            'id': 1,
            'active': True,
            'slug': 'subtask-001',
            'created_by': self.user.id,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'maintask': self.maintask.id,
            'title': 'Subtask #001'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubtaskDetailTest(TestCaseBase):
    url = reverse('subtask-detail', args=['subtask-42'])

    def test_obj_get(self):
        self.client.credentials(**self.jwt_token)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubTask.objects.count(), 1)
    
    def test_obj_patch(self):
        self.client.credentials(**self.jwt_token)
        response = self.client.patch(self.url, kwargs={'active': False}, format='json')
        response_data = json.loads(response.content)
        task = SubTask.objects.get(slug='subtask-42')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('active'), task.active)

    def test_obj_delete(self):
        self.client.credentials(**self.jwt_token)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)