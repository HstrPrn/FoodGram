from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, TagViewSet


recipes_router = DefaultRouter()
recipes_router.register('tags', TagViewSet)
recipes_router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(recipes_router.urls))
]