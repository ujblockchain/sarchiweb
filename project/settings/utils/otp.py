from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django_otp import devices_for_user, match_token, login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice 
from project.settings import env

ADMIN_PATH = env.get('ADMIN_PATH')

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'

    def form_valid(self, form):
        user = form.get_user()
        otp_token = (self.request.POST.get('otp_token') or '').strip()

        if not otp_token:
            messages.error(self.request, 'Please enter your two-factor code.')
            return self.render_to_response(self.get_context_data(form=form))

        # returns the device object if valid, or none if invalid.
        device = match_token(user, otp_token)
        
        if device:
            login(self.request, user)
            otp_login(self.request, device)

            # honor ?next= parameter
            next_url = self.request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect(f'/{ADMIN_PATH}/')

        has_totp = any(isinstance(d, TOTPDevice) for d in devices_for_user(user, confirmed=True))
        msg = 'Invalid TOTP code.' if has_totp else 'Invalid backup code or two-factor token.'
        messages.error(self.request, msg)

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['otp_required'] = True
        context['next'] = self.request.GET.get('next', '')
        return context