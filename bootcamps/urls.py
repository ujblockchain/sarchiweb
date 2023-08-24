from django.urls import path
from .views import BootcampView

urlpatterns = [
    path('registration/', BootcampView.as_view(), name='bootcamp')
]
