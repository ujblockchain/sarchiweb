from django.urls import path
from .views import CommunityRegistrationView

urlpatterns = [
    path('signup', CommunityRegistrationView.as_view(), name='community_form'),
]
