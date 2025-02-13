from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from core.contact.forms import UserMessageForm
from core.newsletters.forms import NewsletterEmailForm
from core.partners.models import Partners

from .forms import ProgramForm
from .models import ProgramConfig, ProgramSignUp

# get the current time in UTC
current_timestamp = timezone.now()


class ProgramView(View):

    def get(self, request, *args, **kwargs):

        # set template
        template_name = 'forms/program-form.html'
        # get latest record
        program_config = ProgramConfig.objects.order_by('-date_created').filter(Q(closing_date__gte=current_timestamp))

        # init context
        context = {
            'form':
                UserMessageForm(),
            'program_form':
                ProgramForm(),
            'partners':
                Partners.objects.filter(publish=True),
            # newsletter form
            'newsletter_form':
                NewsletterEmailForm(),
            # program settings
            'registration_open':
                current_timestamp > program_config[0].opening_date if program_config.exists() else False,
            'registration_closed':
                current_timestamp > program_config[0].closing_date if program_config.exists() else False
        }

        # render template
        return render(request, template_name, context)

    # post request
    def post(self, request, *args, **kwargs):

        form = ProgramForm(request.POST)

        # check if request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if form is valid
            if form.is_valid():
                cleaned_data = form.cleaned_data()
                email = form.cleaned_data['email']

                # check if applicant has register before
                if ProgramConfig.objects.filter(
                    Q(email=email) & Q(date_created__month=9) & Q(date_created__year=2024)
                ).exists():
                    return JsonResponse({
                        'message': 'duplicate_error',
                        'error': 'You have already registered for this event!',
                    })
                else:
                    # get program settings
                    program_config = ProgramConfig.objects.order_by('-date_created').filter(
                        Q(closing_date__gte=current_timestamp)
                    )

                    # create model instance
                    ProgramSignUp.objects.create(**cleaned_data, program_config=program_config[0])

                    return JsonResponse({
                        'message': 'success',
                        'status': 'Thank You. Your Application has been Submitted Successfully.',
                    })

            else:
                return JsonResponse({'message': 'error', 'error': form.errors})
