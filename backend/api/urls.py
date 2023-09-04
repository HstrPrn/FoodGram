from django.urls import include, path

from recipes.urls import recipes_patterns


urlpatterns = [
    path('', include(recipes_patterns))
]
