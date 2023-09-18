from django.urls import include, path

from recipes.urls import recipe_url_patterns
from users.urls import users_urlpatterns

urlpatterns = [
    path('', include(recipe_url_patterns)),
    path('', include(users_urlpatterns)),
]
