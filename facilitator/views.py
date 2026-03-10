import datetime
from django.views import View
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from .forms import StudentApplicationForm


class StudentRegistrationView(View):
    template_name = 'forms/facilitator.html'
    form_class = StudentApplicationForm

    def get(self, request, *args, **kwargs):
        deadline = datetime.date(2026, 3, 31)
        context = {
            'registration_open': timezone.now().date() < deadline,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)

            if form.is_valid():
                form.save()
                return JsonResponse(
                    {'success': True, 'message': 'Application successful!'}
                )
            else:
                print(form.errors)
                return JsonResponse(
                    {'success': False, 'errors': form.errors}, status=400
                )

        return JsonResponse(
            {'success': False, 'error': 'Invalid request type.'}, status=400
        )
