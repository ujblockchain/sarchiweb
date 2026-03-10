from django.urls import path

from .views import StudentRegistrationView

urlpatterns = [
    path('signup', StudentRegistrationView.as_view(), name='facilitator_form'),
]
