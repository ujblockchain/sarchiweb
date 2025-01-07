from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.management import call_command
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

# init user
User = get_user_model()


class RevisionDelete(UserPassesTestMixin, View):

    def post(self, request, *args, **kwargs):
        app_name = request.POST.get('app_name')
        model_name = request.POST.get('model_name')
        path = request.POST.get('path')
        model_name = model_name.replace(' ', '')
        app_name_lower = app_name.lower()
        # call revision command
        call_command('deleterevisions', f'{app_name_lower}.{model_name}', days=30)
        # success message
        messages.success(request, 'Revision(s) deleted successfully')
        # redirect to previous page
        return redirect(path)

    # test for only admin
    def test_user(request):
        return User.objects.filter(is_superuser=True)


class AccountLockout(TemplateView):
    template_name = 'account/lockout.html'
