import datetime

from django.views import View
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from .forms import EventRegistrationForm


class EventRegistrationView(View):
    template_name = 'forms/event.html'
    form_class = EventRegistrationForm

    def get(self, request, *args, **kwargs):
        deadline = datetime.date(2026, 4, 10)
        context = {
            'registration_open': timezone.now().date() < deadline,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)

            if form.is_valid():
                form.cleaned_data.pop('media_consent', None)
                form.save()
                return JsonResponse(
                    {'success': True, 'message': 'Application successful!'}
                )
            else:
                return JsonResponse(
                    {'success': False, 'errors': form.errors}, status=400
                )

        return JsonResponse(
            {'success': False, 'error': 'Invalid request method.'}, status=400
        )
