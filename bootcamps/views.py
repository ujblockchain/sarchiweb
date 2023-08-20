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
