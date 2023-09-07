from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, TemplateView


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


class NewsletterConfirmUnsubscribe(View):
    ## get id as params
    def get(self, request, id=''):
        # check if email exist
        if NewsletterEmail.objects.filter(id=id).exists():
            # context
            context = {'email_id': id}
            # render template
            return render(request, "newsletter/confirm-unsubscribe.html", context)
        else:
            raise Http404


class NewsletterEmailUnsubscribe(View):
    # get id as params
    def get(self, request, id=''):
        # check if email exist
        if NewsletterEmail.objects.filter(id=id).exists:
            # delete email
            NewsletterEmail.objects.get(id=id).delete()

            # redirect to unsubscribe page
            return HttpResponseRedirect(reverse('newsletter_unsubscribe_done'))
        else:
            raise Http404