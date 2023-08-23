from django.urls import path
from .views import NewsletterView

urlpatterns = [
    path('', NewsletterView.as_view(), name='newsletter_signup'),
]
