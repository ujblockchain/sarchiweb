from django.urls import path
from .views import EventRegistrationView

urlpatterns = [
    path('registration', EventRegistrationView.as_view(), name='event_form'),
]
