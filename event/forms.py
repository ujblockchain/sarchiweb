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

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = phone.replace(" ", "").replace("+", "")

        if not cleaned_phone.isdigit():
            raise forms.ValidationError("Phone number must contain only numbers.")

        if len(cleaned_phone) < 9:
            raise forms.ValidationError("Phone number is too short.")

        return phone
