from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView
from contact.forms import UserMessageForm


# index page view
class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserMessageForm()
        return context
