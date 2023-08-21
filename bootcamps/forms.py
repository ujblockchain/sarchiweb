from django import forms
from .models import BootcampFirst

applicant_level = (
    ('Select your level', 'Select your level'),
    ('Higher Certificate', 'Higher Certificate'),
    ('Diploma', 'Diploma'),
    ('Honors', 'Honors'),
    ('Undergrad', 'Undergrad'),
    ('Post Graduate', 'Post Graduate'),
    ('Others', 'Others'),
)


class BootcampForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    faculty = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Faculty'})
    )
    department = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'})
    )
    level = forms.CharField(
        widget=forms.Select(
            choices=applicant_level, attrs={'class': 'form-control', 'aria-label': 'Default select'}
        ),
    )

    expectation = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Expectation', 'row': 5})
    )

    class Meta:
        model = BootcampFirst
        fields = [
            'first_name',
            'last_name',
            'email',
            'faculty',
            'department',
            'level',
            'expectation',
        ]
