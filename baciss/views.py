from django.views.generic import TemplateView


class BacissAIView(TemplateView):
    template_name = 'pages/baciss-ai-doc.html'


class BacissSupportView(TemplateView):
    template_name = 'pages/baciss-support.html'
