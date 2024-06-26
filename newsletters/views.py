from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache


from .models import NewsletterEmail
from .forms import NewsletterEmailForm
from django.http import Http404


@method_decorator([never_cache,], name='dispatch')
class NewsletterView(View):
    def post(self, request, *args, **kwargs):
        form = NewsletterEmailForm(request.POST)

        # check if form is valid
        if form.is_valid():

            # init model instance
            NewsletterEmail.objects.update_or_create(email=form.cleaned_data['email'])

            # sent success message
            messages.add_message(
                request,
                messages.SUCCESS,
                'Thank You. You Have Been Added to Our Mailing List.',
                extra_tags='newsletter',
            )

            # redirect to form section
            return HttpResponseRedirect('/#newsletter')
        else:
            # raise exception
            messages.add_message(
                request,
                messages.ERROR,
                'Invalid Email Address. Enter A Valid Email.',
                extra_tags='newsletter',
            )

            # redirect to form section
            return HttpResponseRedirect('/#newsletter')


@method_decorator([never_cache,], name='dispatch')
class NewsletterConfirmUnsubscribe(View):
    ## get id as params
    def get(self, request, *args, **kwargs):

        # get id
        id = kwargs.get('id', '')

        # check if email exist
        if NewsletterEmail.objects.filter(id=id).exists():
            # context
            context = {'email_id': id}
            # render template
            return render(request, "newsletter/confirm-unsubscribe.html", context)
        else:
            raise Http404


@method_decorator([never_cache,], name='dispatch')
class NewsletterEmailUnsubscribe(View):
    # get id as params
    def get(self, request, *args, **kwargs):

        # get id
        id = kwargs.get('id', '')

        # check if email exist
        if NewsletterEmail.objects.filter(id=id).exists:
            # delete email
            NewsletterEmail.objects.get(id=id).delete()

            # redirect to unsubscribe page
            return HttpResponseRedirect(reverse('newsletter_unsubscribe_done'))
        else:
            raise Http404


@method_decorator(cache_control(max_age=3600), name='dispatch')
class NewsletterUnsubscribeDone(TemplateView):
    template_name = "newsletter/unsubscribe.html"
