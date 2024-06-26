from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from .models import UserContact
from .forms import UserMessageForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache



@method_decorator([never_cache,], name='dispatch')
class ContactView(View):

    def post(self, request):
        form = UserMessageForm(request.POST)

        try:
            # check if form is valid
            if form.is_valid():
                # init model instance
                contact = UserContact(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    message=form.cleaned_data['message'],
                )

                # check if error exist in form
                contact.clean_fields()

                # save form
                contact.save()

                # sent success message
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Thank You. Your Message has been Submitted.',
                    extra_tags='contact',
                )

                # redirect to form section
                return HttpResponseRedirect('/#contact')
            else:
                # raise exception
                raise Exception

        except Exception as e:
            # get the error and send as an error message
            messages.add_message(
                request,
                messages.ERROR,
                {'form_error': form.errors},
                extra_tags='contact',
            )

            # redirect to form section
            return HttpResponseRedirect('/#contact')
