from django.urls import path
from .views import EventRegistrationView, FewsRegistrationView

urlpatterns = [
    path('ccpfews/', FewsRegistrationView.as_view(), name='fews_form'),
    path('registration/', EventRegistrationView.as_view(), name='event_form'),
]
