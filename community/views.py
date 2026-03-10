from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CommunityRegistrationForm


class CommunityRegistrationView(View):
    template_name = 'forms/community.html'
    form_class = CommunityRegistrationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST)

            if form.is_valid():
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
