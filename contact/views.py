from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View

from .forms import UserMessageForm
from .models import UserContact


class ContactView(View):

    def post(self, request):
        form = UserMessageForm(request.POST)

        try:
            # check if form is valid
            if form.is_valid():
                cleaned_data = form.cleaned_data
                # remove captcha field
                cleaned_data.pop('captcha', None)

                # init model instance
                contact = UserContact(**cleaned_data)

                # check if error exist in form
                contact.clean_fields()

                # save form
                contact.save()

                # sent success message
                messages.success(request, 'Thank You. Your Message has been Submitted.', extra_tags='contact')

                # redirect to form section
                return HttpResponseRedirect('/#contact')
            else:
                # raise exception
                raise Exception

        except Exception:
            # get the error and send as an error message
            messages.error(request, {'form_error': form.errors}, extra_tags='contact')

            # redirect to form section
            return HttpResponseRedirect('/#contact')
