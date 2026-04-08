from django import forms
from .models import EventRegistration


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

        if EventRegistration.objects.filter(email=email).exists():
            raise forms.ValidationError("email already signed up.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned_phone = phone.replace(" ", "").replace("+", "")

        if not cleaned_phone.isdigit():
            raise forms.ValidationError("Phone number must contain only numbers.")

        if len(cleaned_phone) < 9:
            raise forms.ValidationError("Phone number is too short.")

        return phone
