from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ..models import MainTask, SubTask


USER = get_user_model()


class MainTaskTest(TestCase):
    def setUp(self):
        user = USER.objects.create_user(
            'johndoe@email.com',
            'johndoepassword'
        )

        MainTask.objects.create(
            id=1,
            active=True,
            slug='title-001',
            created_by=user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            title='Title #001'
        )

    def test_maintask_exists(self):
        maintask_amount = MainTask.objects.count()
        maintask_obj = MainTask.objects.get(id=1)

        self.assertEqual(maintask_amount, 1)
        self.assertEqual(str(maintask_obj), 'Title #001')


class SubTaskTest(TestCase):
    def setUp(self):
        user = USER.objects.create_user(
            'johndoe@email.com',
            'johndoepassword'
        )

        maintask = MainTask.objects.create(
            id=1,
            active=True,
            slug='title-001',
            created_by=user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            title='Title #001'
        )

        SubTask.objects.create(
            id=1,
            active=True,
            slug='subtask-042',
            created_by=user,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            maintask=maintask,
            title='Subtask #042'
        )

    def test_subtask_exists(self):
        subtask_amount = SubTask.objects.count()
        subtask = SubTask.objects.get(id=1)

        self.assertEqual(subtask_amount, 1)
        self.assertEqual(str(subtask), 'Subtask #042')

