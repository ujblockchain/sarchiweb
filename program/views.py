import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.db.models import Q
from contact.forms import UserMessageForm
from newsletters.forms import NewsletterEmailForm
from partners.models import Partners
from settings.models import ProgramSettings
from .forms import ProgramForm
from .models import Program

# get the current time in UTC
current_timestamp = timezone.now()


class ProgramView(View):

    def get(self, request, *args, **kwargs):

        # set template
        template_name = 'forms/program-form.html'
        # get latest record
        program_settings = ProgramSettings.objects.order_by(
            '-date_created').filter(Q(closing_date__gte=current_timestamp))
        

        # init context
        context = {
            'form': UserMessageForm(),
            'program_form': ProgramForm(),
            'partners': Partners.objects.filter(publish=True),
            # newsletter form
            'newsletter_form': NewsletterEmailForm(),
            # program settings
            'registration_open': current_timestamp > program_settings[0].opening_date if program_settings.exists() else False, 
            'registration_closed': current_timestamp > program_settings[0].closing_date if program_settings.exists() else False, 
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
                # init bound form field
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                gender = form.cleaned_data['gender']
                email = form.cleaned_data['email']
                expectation = form.cleaned_data['expectation']
                nationality = form.cleaned_data['nationality']
                phone_number = form.cleaned_data['phone_number']
                organization = form.cleaned_data['organization']

                # check if applicant has register before
                if Program.objects.filter(email=email).exists():
                    return JsonResponse({
                        "message":"duplicate_error",
                        "error": "You have already registered for this event!",
                    })
                else:
                    # get program settings
                    program_settings = ProgramSettings.objects.order_by(
                        '-date_created').filter(Q(
                            closing_date__gte=current_timestamp))

                    # create model instance
                    Program.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        email=email,
                        nationality=nationality,
                        expectation=expectation,
                        phone_number=phone_number,
                        organization=organization,
                        program_settings=program_settings[0])

                    return JsonResponse({
                        "message": "success",
                        "status": "Thank You. Your Application has been Submitted Successfully.",
                    })

            else:
                return JsonResponse({"message": "error", "error": form.errors})
