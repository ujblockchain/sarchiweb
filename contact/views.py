from django.contrib import messages
from django.shortcuts import redirect

from .forms import ContactForm


class ContactFormMixin:
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect(f"{request.path}#contact")
        else:
            self._invalid_contact_form = form
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self, '_invalid_contact_form'):
            context['form'] = self._invalid_contact_form
            del self._invalid_contact_form
        else:
            context['form'] = ContactForm()

        return context
