from django.contrib import admin
from django.urls import path, include

from .views import LoginAPIView, UserViewSet, ProfileUpdateAPIView, ActivityListAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(
        {'post': 'post'}
    )),
    path('register/', UserViewSet.as_view(
        {'post': 'create'}
    )),

    path('', UserViewSet.as_view(
        {'get': 'list'}
    )),

    path('profile/', ProfileUpdateAPIView.as_view(
        {'patch': 'partial_update'}
    )),

    path('<int:pk>/', UserViewSet.as_view(
        {'get': 'retrieve'},
    )),

    path('activities/', ActivityListAPIView.as_view())


]
