from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.urls import urlpatterns as api_urls


admin.site.site_header = 'Foodgram'
admin.site.site_title = 'Foodgram'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
