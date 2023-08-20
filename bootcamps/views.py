import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View

from contact.forms import UserMessageForm
from .forms import BootcampForm
from .models import BootcampFirst


class BootcampView(View):
    def get(self, request):
        # set template
        template_name = 'forms/training-form.html'

        # init context
        context = {'form': UserMessageForm(), 'training_form': BootcampForm()}

        return render(request, template_name, context)

    # post request
    def post(self, request):
        form = BootcampForm(request.POST)

        # check if request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            # check if form is valid
            if form.is_valid():

                # init bound form field
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                faculty = form.cleaned_data['faculty']
                department = form.cleaned_data['department']
                level = form.cleaned_data['level']
                expectation = form.cleaned_data['expectation']

                # check if applicant has register before
                if BootcampFirst.objects.filter(email=email).exists():
                    return JsonResponse(
                        {
                            "message": "duplicate_error",
                            "error": "You have already registered for the Bootcamp!",
                        }
                    )
                else:
                    # create model instance
                    BootcampFirst.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        faculty=faculty,
                        department=department,
                        level=level,
                        expectation=expectation,
                    )

                    return JsonResponse(
                        {
                            "message": "success",
                            "status": "Thank You. Your Application has been Submitted Successfully",
                        }
                    )

            else:
                return JsonResponse({"message": "error", "error": form.errors})
