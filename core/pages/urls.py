from django.urls import path

from .views import EventView, HomeView

urlpatterns = [
    path('mb', EventView.as_view(), name='mb_home'),
    path('', HomeView.as_view(), name='home'),
]
