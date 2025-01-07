from django.urls import path

from .views import MasterclassView

urlpatterns = [
    path('registration/', MasterclassView.as_view(), name='bootcamp'),
]
