from django.shortcuts import render
from django.views.generic import TemplateView


# index page view
class HomeView(TemplateView):
    template_name = "pages/index.html"
