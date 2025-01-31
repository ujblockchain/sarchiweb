import validators
from django import forms

from core.bootcamps.forms import applicant_level, gender, updated_nationality_list

from .models import Masterclass


class MasterclassForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        }),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        }),
    )
    gender = forms.CharField(
        required=True,
        widget=forms.Select(choices=gender, attrs={
            'class': 'form-control',
            'aria-label': 'Default select'
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
    )
    faculty = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Faculty'
        }),
    )
    department = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Department'
        }),
    )
    level = forms.CharField(
        required=True,
        widget=forms.Select(choices=applicant_level, attrs={
            'class': 'form-control',
            'aria-label': 'Default select'
        }),
    )
    student_number = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Student Number'
        }),
    )

    nationality = forms.CharField(
        required=True,
        widget=forms.Select(
            choices=updated_nationality_list, attrs={
                'class': 'form-control',
                'aria-label': 'Default select'
            }
        ),
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
        }),
    )

    repo_link = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Github Repo Link (https://github.com/...)',
            }
        ),
    )
    expectation = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Expectation',
            'row': 5
        }),
    )

    class Meta:
        model = Masterclass
        fields = [
            'first_name', 'last_name', 'gender', 'email', 'faculty', 'department', 'level', 'student_number',
            'nationality', 'phone_number', 'expectation', 'repo_link'
        ]

    def clean_email(self):
        # get input value form clean_data dict
        value = self.cleaned_data['email']
        # Check if the value already exist
        if Masterclass.objects.filter(email=value).exists():
            raise forms.ValidationError('You have already registered with this email.', code='email')
        return value

    def clean_repo_link(self):
        # get input value form clean_data dict
        repo_link = self.cleaned_data['repo_link']

        # Check if the value already exist
        if 'github.com' not in repo_link or validators.url(repo_link) is False:
            raise forms.ValidationError('Enter a valid Github link.', code='repo_link')

        return repo_link
