from django.urls import path

from .views import AccountLockout, RevisionDelete

urlpatterns = [
    path('revision/delete/', RevisionDelete.as_view(), name='rev_delete'),
    path('user/locked/', AccountLockout.as_view(), name='lockout'),
]
