from django.urls import path
from .views import (
    NewsletterView,
    NewsletterEmailUnsubscribe,
    NewsletterConfirmUnsubscribe,
    NewsletterUnsubscribeDone,
)

urlpatterns = [
    path('', NewsletterView.as_view(), name='newsletter_signup'),
    path('unsubscribe/<str:id>', NewsletterEmailUnsubscribe.as_view(), name='newsletter_unsubscribe'),
    path(
        'unsubscribe/<str:id>/confirm',
        NewsletterConfirmUnsubscribe.as_view(),
        name='newsletter_confirm',
    ),
    path('unsubscribe', NewsletterUnsubscribeDone.as_view(), name='newsletter_unsubscribe_done'),
]
