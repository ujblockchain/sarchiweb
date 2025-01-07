from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from core.contact.forms import UserMessageForm
from core.newsletters.forms import NewsletterEmailForm
from core.partners.models import Partners

from .forms import BootcampForm
from .models import BootcampConfig, BootcampSignup

# get the current time in UTC
current_timestamp = timezone.now()


class BootcampView(View):

    def get(self, request, *args, **kwargs):
        # set template
        template_name = 'forms/bootcamp.html'

        # get latest record
        bootcamp_settings = BootcampConfig.objects.order_by('-date_created').filter(
            Q(closing_date__gte=current_timestamp)
        )

        # init context
        context = {
            'form':
                UserMessageForm(),
            'training_form':
                BootcampForm(),
            'partners':
                Partners.objects.filter(publish=True),
            'newsletter_form':
                NewsletterEmailForm(),
            'registration_open':
                current_timestamp > bootcamp_settings[0].opening_date if bootcamp_settings.exists() else False,
            'registration_closed':
                current_timestamp > bootcamp_settings[0].closing_date if bootcamp_settings.exists() else False
        }

        return render(request, template_name, context)

    # post request
    def post(self, request, *args, **kwargs):
        form = BootcampForm(request.POST)

        # check if request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            # check if form is valid
            if form.is_valid():
                # clean form
                cleaned_data = form.cleaned_data
                # update value
                if cleaned_data['can_you_code'] == 'Can you code in HTML, CSS & Python':
                    cleaned_data['can_you_code'] = 'No I can not code in HTML, CSS & Python'
                else:
                    cleaned_data['can_you_code'] = form.cleaned_data['can_you_code']

                # get bootcamp settings
                bootcamp_settings = BootcampConfig.objects.order_by('-date_created').filter(
                    Q(closing_date__gte=current_timestamp)
                )

                # create model instance
                BootcampSignup.objects.create(**cleaned_data, bootcamp_settings=bootcamp_settings[0])

                return JsonResponse({
                    'message': 'success',
                    'status': 'Thank You. Your Application has been Submitted Successfully.',
                })

            else:
                return JsonResponse({'message': 'error', 'error': form.errors})
