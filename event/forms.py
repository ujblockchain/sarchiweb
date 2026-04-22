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
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'faculty',
            'department',
            'nationality',
            'year_of_study',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        # calculate the exact time 5 days ago from right now
        five_days_ago = timezone.now() - timedelta(days=5)

        # check if the email exists and was created within the last 5 days
        if EventRegistration.objects.filter(
            email=email, created_at__gte=five_days_ago
        ).exists():
            raise forms.ValidationError("This email has already been registered.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = phone.replace(" ", "").replace("+", "")

        if not cleaned_phone.isdigit():
            raise forms.ValidationError("Phone number must contain only numbers.")

        if len(cleaned_phone) < 9:
            raise forms.ValidationError("Phone number is too short.")

        return phone


class FewsRegistrationForm(forms.ModelForm):
    media_consent = forms.BooleanField(
        required=True, error_messages={'required': 'You must accept the disclaimer.'}
    )

    class Meta:
        model = FewsRegistration
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'organization',
            'attendance_type',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        five_days_ago = timezone.now() - timedelta(days=5)

        if EventRegistration.objects.filter(
            email=email, created_at__gte=five_days_ago
        ).exists():
            raise forms.ValidationError("This email has already been registered.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = phone.replace(" ", "").replace("+", "")

        if not cleaned_phone.isdigit():
            raise forms.ValidationError("Phone number must contain only numbers.")

        if len(cleaned_phone) < 9:
            raise forms.ValidationError("Phone number is too short.")

        return phone
