from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import MainTask, SubTask


USER = get_user_model()


class TestCaseBase(TestCase):
    def setUp(self):
        USER.objects.create_superuser(
            email='johndoe@email.com',
            password='johndoepassword'
        )

    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = USER.objects.get(email='johndoe@email.com')

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION":f'Bearer {refresh.access_token}'}


class MainTaskTest(TestCaseBase):
    url = reverse('maintask-list')

    def test_get_obj(self):
        self.client.get(self.url, **self.bearer_token)

    def test_create_obj(self):
        data = {
            'id': 1,
            'active': True,
            'slug': 'maintask-042',
            'created_by': 1,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'title': 'Maintask #042'
        }

        response = self.client.post(self.url, data, format='json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MainTask.objects.count(), 1)
        self.assertEqual(MainTask.objects.get().title, 'Maintask #042')