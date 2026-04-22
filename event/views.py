from django.views import View
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse

from event.models import EventEmailConfig
from .forms import EventRegistrationForm, FewsRegistrationForm


class EventRegistrationView(View):
    template_name = 'forms/event.html'
    form_class = EventRegistrationForm

    def get(self, request, *args, **kwargs):
        deadline = (
            EventEmailConfig.objects.filter(event_type__icontains='ujb')
            .values_list('registration_end_time', flat=True)
            .first()
        )

        if deadline:
            is_open = timezone.now().date() < deadline.date()
        else:
            is_open = False

        context = {
            'registration_open': is_open,
            'form': self.form_class(),
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


class FewsRegistrationView(View):
    template_name = 'forms/fews.html'
    form_class = FewsRegistrationForm

    def get(self, request, *args, **kwargs):
        deadline = (
            EventEmailConfig.objects.filter(event_type__icontains='fews')
            .values_list('registration_end_time', flat=True)
            .first()
        )

        if deadline:
            is_open = timezone.now().date() < deadline.date()
        else:
            is_open = False

        context = {
            'registration_open': is_open,
            'form': self.form_class(),
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
