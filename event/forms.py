from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import EventRegistration, FewsRegistration


class EventRegistrationForm(forms.ModelForm):
    media_consent = forms.BooleanField(
        required=True, error_messages={'required': 'You must accept the disclaimer.'}
    )

    class Meta:
        model = EventRegistration
        fields = [  # noqa: RUF012
            'first_name',
            'last_name',
            'email',
            'phone',
            'faculty',
            'department',
            'nationality',
            'year_of_study',
            'learning_path',
            'repository_link',
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = phone.replace(' ', '').replace('+', '')

        if not cleaned_phone.isdigit():
            raise forms.ValidationError('Phone number must contain only numbers.')

        if len(cleaned_phone) < 9:
            raise forms.ValidationError('Phone number is too short.')

        return phone

    def clean_email(self):
        user_email = self.cleaned_data.get('email')
        five_days_ago = timezone.now() - timedelta(days=5)

        # check if this email registered in the last 5 days
        if EventRegistration.objects.filter(
            email=user_email, created_at__gte=five_days_ago
        ).exists():
            raise forms.ValidationError('Already registered for the event.')

        return user_email

    def clean_learning_path(self):
        learning_path = self.cleaned_data.get('learning_path')

        if learning_path != 'coding' and learning_path != 'drag_drop':
            raise forms.ValidationError('Select a valid Session.')

        return learning_path

    def clean_repository_link(self):
        learning_path = self.cleaned_data.get('learning_path')
        repository_link = self.cleaned_data.get('repository_link')

        if repository_link:
            repository_link = repository_link.strip()

        if repository_link is None and learning_path == 'coding':
            raise forms.ValidationError(
                'Repository link is required for the Coding Session.'
            )

        return repository_link


class FewsRegistrationForm(forms.ModelForm):
    media_consent = forms.BooleanField(
        required=True, error_messages={'required': 'You must accept the disclaimer.'}
    )

    class Meta:
        model = FewsRegistration
        fields = [  # noqa: RUF012
            'first_name',
            'last_name',
            'email',
            'phone',
            'organization',
            # 'attendance_type',
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = phone.replace(' ', '').replace('+', '')

        if not cleaned_phone.isdigit():
            raise forms.ValidationError('Phone number must contain only numbers.')

        if len(cleaned_phone) < 9:
            raise forms.ValidationError('Phone number is too short.')

        return phone
