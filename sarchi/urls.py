from django.contrib import admin
from django.conf import settings
from django.urls import path

urlpatterns = [
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
]
