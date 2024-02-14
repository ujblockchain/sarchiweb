from django import forms
from .modelChoices import nationality_form
from .models import Bootcamp

applicant_level = (
    ('Select Your Level', 'Select Your Level'),
    ('Higher Certificate', 'Higher Certificate'),
    ('Diploma', 'Diploma'),
    ('Year 1', 'Year 1'),
    ('Year 2', 'Year 2'),
    ('Year 3', 'Year 3'),
    ('Year 4', 'Year 4'),
    ('Honours', 'Honours'),
    ('Post Graduate', 'Post Graduate'),
    ('Others', 'Others'),
)


gender = (
    ('Gender', 'Gender'),
    ('Female', 'Female'),
    ('Male', 'Male'),
)

user_can_code = (
    ('Can you code in HTML, CSS & Python', 'Can you code in HTML, CSS & Python'),
    ('Yes I can code in HTML, CSS & Python', 'Yes I can code in HTML, CSS & Python'),
    (
        'No I can not code in HTML, CSS & Python',
        'No I can not code in HTML, CSS & Python',
    ),
)

training_session = (
    ('Select training session', 'Select training session'),
    (
        'No Coding Session (Drag and Drop Design)',
        'No Coding Session (Drag and Drop Design)',
    ),
    (
        'Coding Session (Requires basic knowledge of HTML, CSS & Python)',
        'Coding Session (Requires basic knowledge of HTML, CSS & Python)',
    ),
)


class BootcampForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}
        )
    )
    gender = forms.CharField(
        widget=forms.Select(
            choices=gender,
            attrs={'class': 'form-control', 'aria-label': 'Default select'},
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    faculty = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Faculty'}
        )
    )
    department = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Department'}
        )
    )
    level = forms.CharField(
        widget=forms.Select(
            choices=applicant_level,
            attrs={'class': 'form-control', 'aria-label': 'Default select'},
        ),
    )
    student_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Student Number'}
        )
    )

    nationality = forms.CharField(
        widget=forms.Select(
            choices=nationality_form,
            attrs={'class': 'form-control', 'aria-label': 'Default select'},
        ),
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
        )
    )
    session = forms.CharField(
        widget=forms.Select(
            choices=training_session,
            attrs={'class': 'form-control', 'aria-label': 'Default select'},
        ),
    )

    can_you_code = forms.CharField(
        required=False,
        widget=forms.Select(
            choices=user_can_code,
            attrs={'class': 'form-control', 'aria-label': 'Default select'},
        ),
    )
    repo_link = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={'class': 'form-control', 'placeholder': 'https://...'}
        ),
    )
    expectation = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Expectation', 'row': 5}
        )
    )

    class Meta:
        model = Bootcamp
        fields = [
            'first_name',
            'last_name',
            'gender',
            'email',
            'faculty',
            'department',
            'level',
            'student_number',
            'nationality',
            'phone_number',
            'expectation',
            'session',
            'can_you_code',
            'repo_link',
        ]

    def clean_can_you_code(self):
        # get input value form clean_data dict
        value = self.cleaned_data['can_you_code']
        # Check if the field is not selected
        if value == 'Can you code in HTML, CSS & Python':
            value = 'No I can not code in HTML, CSS & Python'
        # return updated value
        return value

    def clean_email(self):
        # get input value form clean_data dict
        value = self.cleaned_data['email']
        # Check if the value already exist
        if Bootcamp.objects.filter(email=value).exists:
            raise forms.ValidationError(
                'You have already registered with this email.', code='email'
            )
        # return updated value
        return value
