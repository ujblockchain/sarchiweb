from django import forms
from .models import StudentApplication


class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'faculty',
            'department',
            'nationality',
            'year_of_study',
            'ieee_membership',
            'saiee_membership',
        ]

    def clean_email(self):
        value = self.data.get('email')

        if StudentApplication.objects.filter(email=value).exists():
            raise forms.ValidationError("email already signed up.")

        return value

    def clean_ieee_membership(self):
        value = self.data.get('ieee_membership')

        if value != 'yes' and value != 'no':
            raise forms.ValidationError("field is required")
        return True if value == 'yes' else False

    def clean_saiee_membership(self):
        value = self.data.get('saiee_membership')

        if value != 'yes' and value != 'no':
            raise forms.ValidationError("field is required")

        return True if value == 'yes' else False
