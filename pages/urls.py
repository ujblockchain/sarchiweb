from django.urls import path
from .views import HomeView, EventView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
     path('mb', EventView.as_view(), name='home'),
]
