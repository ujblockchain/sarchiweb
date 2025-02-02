import validators
from django import forms

from .models import BootcampSignup
from .utils.modelChoices import nationality

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

gender = (('Gender', 'Gender'), ('Female', 'Female'), ('Male', 'Male'))

user_can_code = (
    ('Can you code in HTML, CSS & Python', 'Can you code in HTML, CSS & Python'),
    ('Yes I can code in HTML, CSS & Python', 'Yes I can code in HTML, CSS & Python'),
    ('No I can not code in HTML, CSS & Python', 'No I can not code in HTML, CSS & Python'),
)

training_session = (
    (
        'Select training session',
        'Select training session',
    ),
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
        widget=forms.Select(choices=nationality, attrs={
            'class': 'form-control',
            'aria-label': 'Default select'
        }),
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
        }),
    )

    session = forms.CharField(
        widget=forms.Select(choices=training_session, attrs={
            'class': 'form-control',
            'aria-label': 'Default select'
        }),
    )

    can_you_code = forms.CharField(
        required=False,
        widget=forms.Select(choices=user_can_code, attrs={
            'class': 'form-control',
            'aria-label': 'Default select'
        }),
    )
    repo_link = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Github Repo Link (https://github.com/...)',
            }
        ),
    )
    expectation = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Expectation',
            'row': 5
        }),
    )

    class Meta:
        model = BootcampSignup
        fields = [
            'first_name', 'last_name', 'gender', 'email', 'faculty', 'department', 'level', 'student_number',
            'nationality', 'phone_number', 'expectation', 'session', 'can_you_code', 'repo_link'
        ]

    def clean_can_you_code(self):
        # get input value form clean_data dict
        value = self.cleaned_data['can_you_code']
        # Check if the field is not selected
        if value == 'Can you code in HTML, CSS & Python':
            value = 'No I can not code in HTML, CSS & Python'

        return value

    def clean_email(self):
        # get input value form clean_data dict
        value = self.cleaned_data['email']
        # Check if the value already exist
        if BootcampSignup.objects.filter(email=value).exists():
            # raise exception
            raise forms.ValidationError('You have already registered with this email.', code='email')
        return value

    def clean_repo_link(self):
        # get input value form clean_data dict
        repo_link = self.cleaned_data['repo_link']
        can_code = self.cleaned_data['can_you_code']

        # check if user said they can code
        if (
            can_code != 'No I can not code in HTML, CSS & Python' and can_code != 'Can you code in HTML, CSS & Python'
        ):
            #
            if not validators.url(repo_link):
                # raise exceptions
                raise forms.ValidationError('Enter a valid repository link.', code='repo')

        return repo_link

    def clean_nationality(self):
        # get input value form clean_data dict
        nationality_choice = self.cleaned_data['nationality']

        # check user selection
        if nationality_choice == 'Select Nationality':
            # raise exceptions
            raise forms.ValidationError('Enter a valid nationality.', code='nationality')

        return nationality_choice
