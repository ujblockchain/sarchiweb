from django.urls import path

from .views import BacissAIView, BacissSupportView

urlpatterns = [
    path('ai-agent/', BacissAIView.as_view(), name='baciss_ai'),
    path('support/', BacissSupportView.as_view(), name='baciss_support'),
]
