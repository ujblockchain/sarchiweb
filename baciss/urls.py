from django.urls import path

from .views import BacissAIView, BacissDOCloudView, BacissNFCloudView, BacissSupportView

urlpatterns = [
    path('ai-agent/', BacissAIView.as_view(), name='baciss_ai'),
    path('support/', BacissSupportView.as_view(), name='baciss_support'),
    path('cloud/digitalocean/', BacissDOCloudView.as_view(), name='baciss_do_cloud'),
    path('cloud/northflank/', BacissNFCloudView.as_view(), name='baciss_nf_cloud'),
]
