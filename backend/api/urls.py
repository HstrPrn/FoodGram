from django.urls import include, path

from recipes.urls import recipe_url_patterns

urlpatterns = [
    path('', include(recipe_url_patterns)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
