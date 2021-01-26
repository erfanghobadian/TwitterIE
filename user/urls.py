from django.contrib import admin
from django.urls import path, include

from .views import LoginAPIView, UserViewSet


urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('register/', UserViewSet.as_view(
        {'post': 'create'}
    )),

    path('', UserViewSet.as_view(
        {'get': 'list'}
    )),
    path('<int:pk>/', UserViewSet.as_view(
        {'get': 'retrieve'}
    )),
]
