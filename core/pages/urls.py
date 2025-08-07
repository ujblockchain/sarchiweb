from django.urls import path

from .views import EventView, HomeView, RView

urlpatterns = [
    path('mb', EventView.as_view(), name='mb_home'),
    path('', HomeView.as_view(), name='home'),
    path('email', RView.as_view(), name='email'),
]
