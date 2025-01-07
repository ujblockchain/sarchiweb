from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView

from .forms import NewsletterEmailForm
from .models import NewsletterEmail


class NewsletterView(View):

    def post(self, request, *args, **kwargs):
        form = NewsletterEmailForm(request.POST)

        # check if form is valid
        if form.is_valid():

            # init model instance
            NewsletterEmail.objects.update_or_create(email=form.cleaned_data['email'])

            # sent success message
            messages.success(request, 'Thank You. You Have Been Added to Our Mailing List.', extra_tags='newsletter')

            # redirect to form section
            return HttpResponseRedirect('/#newsletter')
        else:
            # raise exception
            messages.error(request, 'Invalid Email Address. Enter A Valid Email.', extra_tags='newsletter')

            # redirect to form section
            return HttpResponseRedirect('/#newsletter')


class NewsletterConfirmUnsubscribe(View):
    # get id as params
    def get(self, request, *args, **kwargs):

        # get id
        kwargs_id = kwargs.get('id', '')

        # check if email exist
        if NewsletterEmail.objects.filter(id=kwargs_id).exists():
            # context
            context = {'email_id': kwargs_id}
            # render template
            return render(request, 'newsletter/confirm-unsubscribe.html', context)
        else:
            raise Http404


class NewsletterEmailUnsubscribe(View):
    # get id as params
    def get(self, request, *args, **kwargs):

        # get id
        kwargs_id = kwargs.get('id', '')

        # check if email exist
        if NewsletterEmail.objects.filter(id=kwargs_id).exists:
            # delete email
            NewsletterEmail.objects.get(id=kwargs_id).delete()

            # redirect to unsubscribe page
            return HttpResponseRedirect(reverse('newsletter_unsubscribe_done'))
        else:
            raise Http404


class NewsletterUnsubscribeDone(TemplateView):
    template_name = 'newsletter/unsubscribe.html'
