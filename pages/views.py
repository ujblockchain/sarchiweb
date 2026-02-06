from django.views.generic.base import TemplateView
from contact.views import ContactFormMixin


class AccountLockout(TemplateView):
    template_name = 'pages/lockedout.html'


class HomeView(ContactFormMixin, TemplateView):
    template_name = 'pages/index.html'
