from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView


User = get_user_model()


# test for only admin
def test_user_role(request):
    return User.objects.filter(is_superuser=True)


@user_passes_test(test_user_role)
def revisiondelete(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name')
        model_name = request.POST.get('model_name')
        path = request.POST.get('path')
        model_name = model_name.replace(" ", "")
        app_name_lower = app_name.lower()
        # call revision command
        call_command('deleterevisions', f"{app_name_lower}.{model_name}", days=30)
        # success message
        messages.add_message(request, messages.SUCCESS, 'Revision(s) deleted successfully')
        # redirect to previous page
        return redirect(path)


class AccountLockout(TemplateView):
    template_name = "account/lockout.html"
