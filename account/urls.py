from django.urls import path
from .views import revision_delete, AccountLockout

urlpatterns = [
    path('revision/delete/', revision_delete, name="rev_delete"),
    path('user/locked/', AccountLockout.as_view(), name='lockout'),
]
