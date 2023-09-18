from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


users_router = DefaultRouter()
users_router.register('users', UserViewSet)

users_urlpatterns = [
    path('', include(users_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
