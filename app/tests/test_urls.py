from django.urls import path, include, resolve, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from ..api.views import (
    MainTaskListCreateView, MainTaskRetrieveUpdateDestroyView,
    SubTaskListCreateView, SubTaskRetrieveUpdateDestroyView
)


class MainTaskTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('app.api.urls')),
    ]

    def test_maintasks_is_resolved(self):
        url = reverse('maintask-list')
        self.assertEqual(resolve(url).func.view_class, MainTaskListCreateView)

    def test_maintask_is_resolved(self):
        url = reverse('maintask-detail', args=['maintask-042'])
        self.assertEqual(resolve(url).func.view_class, MainTaskRetrieveUpdateDestroyView)


class SubTaskTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('app.api.urls')),
    ]

    def test_subtasks_is_resolved(self):
        url = reverse('subtask-list')
        self.assertEqual(resolve(url).func.view_class, SubTaskListCreateView)

    def test_subtask_is_resolved(self):
        url = reverse('subtask-detail', args=['subtask-042'])
        self.assertEqual(resolve(url).func.view_class, SubTaskRetrieveUpdateDestroyView)