from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils import timezone

from contact.forms import UserMessageForm
from newsletters.forms import NewsletterEmailForm
from partners.models import Partners
from settings.models import BootcampSettings
from .forms import BootcampForm
from .models import Bootcamp

# get the current time in UTC
current_timestamp = timezone.now()


class BootcampView(View):

    def get(self, request, *args, **kwargs):
        # set template
        template_name = 'forms/bootcamp.html'

        # init bootcamp settings
        # get latest record
        bootcamp_settings = BootcampSettings.objects.order_by(
            '-date_created').filter(Q(
                closing_date__gte=current_timestamp))

        # init context
        context = {
            'form': UserMessageForm(),
            'training_form': BootcampForm(),
            'partners': Partners.objects.filter(publish=True),
            # newsletter form
            'newsletter_form': NewsletterEmailForm(),
            # bootcamp settings
            'registration_open': current_timestamp > bootcamp_settings[0].opening_date if bootcamp_settings.exists() else False,
            'registration_closed': current_timestamp > bootcamp_settings[0].closing_date if bootcamp_settings.exists() else False
        }

        return render(request, template_name, context)

    # post request
    def post(self, request, *args, **kwargs):
        form = BootcampForm(request.POST)

        # check if request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            # check if form is valid
            if form.is_valid():
                # init bound form field
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                gender = form.cleaned_data['gender']
                email = form.cleaned_data['email']
                faculty = form.cleaned_data['faculty']
                department = form.cleaned_data['department']
                level = form.cleaned_data['level']
                student_number = form.cleaned_data['student_number']
                expectation = form.cleaned_data['expectation']
                nationality = form.cleaned_data['nationality']
                phone_number = form.cleaned_data['phone_number']
                session = form.cleaned_data['session']
                repo_link = form.cleaned_data['repo_link']
                if form.cleaned_data[
                        'can_you_code'] == 'Can you code in HTML, CSS & Python':
                    can_you_code = 'No I can not code in HTML, CSS & Python'
                else:
                    can_you_code = form.cleaned_data['can_you_code']

                # get bootcamp settings
                bootcamp_settings = BootcampSettings.objects.order_by(
                    '-date_created').filter(Q(
                        closing_date__gte=current_timestamp))

                # create model instance
                Bootcamp.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    email=email,
                    faculty=faculty,
                    department=department,
                    level=level,
                    student_number=student_number,
                    nationality=nationality,
                    expectation=expectation,
                    phone_number=phone_number,
                    session=session,
                    can_you_code=can_you_code,
                    repo_link=repo_link,
                    bootcamp_settings = bootcamp_settings[0]
                )

                return JsonResponse({
                    "message": "success",
                    "status": "Thank You. Your Application has been Submitted Successfully.",
                })

            else:
                return JsonResponse({"message": "error", "error": form.errors})
