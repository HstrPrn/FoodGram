from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from recipes.views import IngredientViewSet, TagViewSet, RecipeViewSet
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

admin.site.site_header = 'Foodgram'
admin.site.site_title = 'Foodgram'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register(
    'ingredients', IngredientViewSet, basename='ingredients'
)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
