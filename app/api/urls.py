from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .tokens import MyTokenObtainPairView
from .views import (
    MainTaskListCreateView, MainTaskRetrieveUpdateDestroyView,
    SubTaskListCreateView, SubTaskRetrieveUpdateDestroyView,
)


urlpatterns = [
    # Views
    path('maintask/', MainTaskListCreateView.as_view(), name='maintask-list'),
    path('maintask/<slug:slug>/', MainTaskRetrieveUpdateDestroyView.as_view(), name='maintask-detail'),
    path('subtask/', SubTaskListCreateView.as_view(), name='subtask-list'),
    path('subtask/<slug:slug>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'),
    # Tokens
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]