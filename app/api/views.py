from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import MainTaskSerializer, SubTaskSerializer
from ..models import MainTask, SubTask


class MainTaskListCreateView(ListCreateAPIView):
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer
    pagination_class = PageNumberPagination


class MainTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = MainTask.objects.all()
    serializer_class = MainTaskSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.select_related('maintask').all()
    serializer_class = SubTaskSerializer
    pagination_class = PageNumberPagination


class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.select_related('maintask').all()
    serializer_class = SubTaskSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination