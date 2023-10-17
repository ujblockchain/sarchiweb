from django import forms
from bootcamps.modelChoices import nationality_form
from .models import Program


gender = (
    ('Gender', 'Gender'),
    ('Female', 'Female'),
    ('Male', 'Male'),
)


class ProgramForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    gender = forms.CharField(
        widget=forms.Select(
            choices=gender, attrs={'class': 'form-control', 'aria-label': 'Default select'}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    nationality = forms.CharField(
        widget=forms.Select(
            choices=nationality_form,
            attrs={'class': 'form-control', 'aria-label': 'Default select'},
        ),
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    expectation = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Expectation', 'row': 5}
        )
    )

    class Meta:
        model = Program
        fields = [
            'first_name',
            'last_name',
            'gender',
            'email',
            'nationality',
            'phone_number',
            'expectation',
        ]
