from typing import Any
from django import forms
from bootcamps.modelChoices import nationality
from .models import Program

gender = (('Gender', 'Gender'), ('Female', 'Female'), ('Male', 'Male'))


class ProgramForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        }))
    gender = forms.CharField(widget=forms.Select(
        choices=gender,
        attrs={
            'class': 'form-control',
            'aria-label': 'Default select',
        },
    ))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    nationality = forms.CharField(widget=forms.Select(
        choices=nationality,
        attrs={
            'class': 'form-control',
            'aria-label': 'Default select'
        },
    ), )
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        }))
    organization = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Organization'
        }))
    expectation = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Expectation',
            'row': 5
        }))

    class Meta:
        model = Program
        fields = [
            'first_name', 'last_name', 'gender', 'email', 'nationality',
            'phone_number', 'organization', 'expectation'
        ]

    def clean_nationality(self):
        # get input value form clean_data dict
        nationality_choice = self.cleaned_data['nationality']

        # check user selection
        if nationality_choice == 'Select Nationality':
            # raise exceptions
            raise forms.ValidationError('Enter a valid nationality.',
                                        code='nationality')

        return nationality_choice
