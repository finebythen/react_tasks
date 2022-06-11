from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


USER = get_user_model()


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
        response = self.client.post(reverse('token_obtain_pair'), self.data, format='json')
        token = response.data['access']
        return {"HTTP_AUTHORIZATION": f"JWT {token}"}


class MainTaskTest(TestCaseBase):
    url_verification = reverse('token_obtain_pair')
    url_maintasks = reverse('maintask-list')

    def setUp(self):
        self.email = 'johndoe@email.com'
        self.password = 'johndoepassword'
        self.data = {
            'email': self.email,
            'password': self.password
        }
        USER.objects.create_user(email=self.email, password=self.password)

    def test_auth_user(self):
        response = self.client.post(self.url_verification, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_get_obj(self):
        self.client.credentials(**self.jwt_token)
        
        response = self.client.get(self.url_maintasks, format='json')
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

        response = self.client.post(self.url_maintasks, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)