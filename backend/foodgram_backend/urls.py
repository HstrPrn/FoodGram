from django.contrib import admin
from django.urls import path


admin.site.site_header = 'Foodgram'
admin.site.site_title = 'Foodgram'

urlpatterns = [
    path('admin/', admin.site.urls),
]
