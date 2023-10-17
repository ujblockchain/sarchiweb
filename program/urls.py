from django.urls import path
from .views import ProgramView

urlpatterns = [
    path('registration/', ProgramView.as_view(), name='program')
]
