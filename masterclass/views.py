from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from contact.forms import UserMessageForm
from newsletters.forms import NewsletterEmailForm
from partners.models import Partners
from settings.models import MasterclassSettings
from .forms import MasterclassForm
from .models import Masterclass



# get the current time in UTC
current_timestamp = timezone.now()


class MasterclassView(View):

    def get(self, request, *args, **kwargs):
        # set template
        template_name = 'forms/masterclass.html'
  

        # init bootcamp settings
        # get latest record
        masterclass_settings = MasterclassSettings.objects.order_by(
            '-date_created').filter(Q(closing_date__gte=current_timestamp.now()))
        

        # init context
        context = {
            'form': UserMessageForm(), 
            'training_form': MasterclassForm(), 
            'partners': Partners.objects.filter(publish=True),
            # newsletter form 
            'newsletter_form': NewsletterEmailForm(),
            # bootcamp settings 
            'registration_open': current_timestamp > masterclass_settings[0].opening_date if masterclass_settings.exists() else False, 
            'registration_closed': current_timestamp > masterclass_settings[0].closing_date if masterclass_settings.exists() else False
        }

        return render(request, template_name, context)

    # post request
    def post(self, request, *args, **kwargs):
        form = MasterclassForm(request.POST)

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
                repo_link = form.cleaned_data['repo_link']

                
                # init bootcamp settings
                # get latest record
                masterclass_settings = MasterclassSettings.objects.order_by(
                    '-date_created').filter(Q(closing_date__gte=current_timestamp.now()))

                # create model instance
                Masterclass.objects.create(
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
                    repo_link=repo_link,
                    masterclass_settings = masterclass_settings[0]
                )

                return JsonResponse({
                    "message": "success",
                    "status": "Thank You. Your Application has been Submitted Successfully.",
                })

            else:
                return JsonResponse({"message": "error", "error": form.errors})
