from django.views.generic.base import TemplateView

class AccountLockout(TemplateView):
    template_name = 'account/lockout.html'

    
class HomeView(TemplateView):
    template_name = 'pages/index.html'