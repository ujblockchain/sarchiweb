import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View

from contact.forms import UserMessageForm
from newsletters.forms import NewsletterEmailForm
from partners.models import Partners
from .forms import ProgramForm
from .models import Program


class ProgramView(View):
    def get(self, request):
        # set template
        template_name = 'forms/program-form.html'

        # init context
        context = {
            'form': UserMessageForm(),
            'program_form': ProgramForm(),
            'partners': Partners.objects.filter(publish=True),
            # newsletter form
            'newsletter_form': NewsletterEmailForm(),
        }

        # render template
        return render(request, template_name, context)

    # post request
    def post(self, request):
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
                    return JsonResponse(
                        {
                            "message": "duplicate_error",
                            "error": "You have already registered for the Bootcamp!",
                        }
                    )
                else:
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
                    )

                    return JsonResponse(
                        {
                            "message": "success",
                            "status": "Thank You. Your Application has been Submitted Successfully.",
                        }
                    )

            else:
                return JsonResponse({"message": "error", "error": form.errors})
