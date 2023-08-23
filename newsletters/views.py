from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import View
from .models import NewsletterEmail
from .forms import NewsletterEmailForm
from django.http import Http404


class NewsletterView(View):
    def post(self, request):
        form = NewsletterEmailForm(request.POST)

        # check if form is valid
        if form.is_valid():
            # init model instance
            NewsletterEmail.objects.update_or_create(
                email=form.cleaned_data['email'],
            )

            # sent success message
            messages.add_message(
                request, messages.SUCCESS, 'Thank You. You Have Been Added to Our Mailing List.'
            )

            # redirect to form section
            return HttpResponseRedirect('/#newsletter')
        else:
            # raise exception
            messages.add_message(request, messages.ERROR, 'Invalid Email Address.')

            # redirect to form section
            return HttpResponseRedirect('/#newsletter')


class NewsletterEmailUnsubscribe(View):
    def get(self, request):
        # get user email
        email = self.kwargs.get('user_email')

        # check if email exist
        if NewsletterEmail.objects.filter(email=email).exists:
            # delete email
            NewsletterEmail.objects.get(email=email).delete()

            # redirect to form section
            return HttpResponseRedirect('/#newsletter')
        else:
            raise Http404
