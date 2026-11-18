from django.views.generic import TemplateView


class BacissAIView(TemplateView):
    template_name = 'pages/baciss-ai-doc.html'


class BacissSupportView(TemplateView):
    template_name = 'pages/baciss-support.html'


class BacissDOCloudView(TemplateView):
    template_name = 'pages/baciss-cloud-do-doc.html'


class BacissNFCloudView(TemplateView):
    template_name = 'pages/baciss-cloud-nf-doc.html'


class BacissAzureCloudView(TemplateView):
    template_name = 'pages/baciss-cloud-azure-doc.html'
