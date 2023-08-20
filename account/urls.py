from django.urls import path
from .views import revisiondelete, AccountLockout

urlpatterns = [
    path('revision/delete', revisiondelete, name="rev_delete"),
]
