from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from core.contact.forms import UserMessageForm
from core.newsletters.forms import NewsletterEmailForm
from core.partners.models import Partners

from .forms import MasterclassForm
from .models import Masterclass, MasterclassConfig

# get the current time in UTC
current_timestamp = timezone.now()


class MasterclassView(View):

    def get(self, request, *args, **kwargs):
        # set template
        template_name = 'forms/masterclass.html'

        # init bootcamp settings
        # get latest record
        masterclass_config = MasterclassConfig.objects.order_by('-date_created').filter(
            Q(closing_date__gte=current_timestamp.now())
        )

        # init context
        context = {
            'form':
                UserMessageForm(),
            'training_form':
                MasterclassForm(),
            'partners':
                Partners.objects.filter(publish=True),
            # newsletter form
            'newsletter_form':
                NewsletterEmailForm(),
            # bootcamp settings
            'registration_open':
                current_timestamp > masterclass_config[0].opening_date if masterclass_config.exists() else False,
            'registration_closed':
                current_timestamp > masterclass_config[0].closing_date if masterclass_config.exists() else False
        }

        return render(request, template_name, context)

    # post request
    def post(self, request, *args, **kwargs):
        form = MasterclassForm(request.POST)

        # check if request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            # check if form is valid
            if form.is_valid():
                cleaned_data = form.cleaned_data

                # get latest  bootcamp settings
                masterclass_config = MasterclassConfig.objects.order_by('-date_created').filter(
                    Q(closing_date__gte=current_timestamp.now())
                )

                # create model instance
                Masterclass.objects.create(**cleaned_data, masterclass_settings=masterclass_config[0])

                return JsonResponse({
                    'message': 'success',
                    'status': 'Thank You. Your Application has been Submitted Successfully.',
                })

            else:
                return JsonResponse({'message': 'error', 'error': form.errors})
