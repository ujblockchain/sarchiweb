from django.urls import path

from .views import NewsletterConfirmUnsubscribe, NewsletterEmailUnsubscribe, NewsletterUnsubscribeDone, NewsletterView

urlpatterns = [
    path('unsubscribe/<str:id>/confirm', NewsletterConfirmUnsubscribe.as_view(), name='newsletter_confirm'),
    path('unsubscribe/<str:id>', NewsletterEmailUnsubscribe.as_view(), name='newsletter_unsubscribe'),
    path('unsubscribe', NewsletterUnsubscribeDone.as_view(), name='newsletter_unsubscribe_done'),
    path('', NewsletterView.as_view(), name='newsletter_signup'),
]
