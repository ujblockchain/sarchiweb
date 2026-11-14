from django.urls import path

from .views import BacissAIView

urlpatterns = [
    path('ai-agent/', BacissAIView.as_view(), name='baciss_ai'),
]
