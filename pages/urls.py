from django.urls import path

from .views import AccountLockout, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('user/locked/', AccountLockout.as_view(), name='lockout'),
]
