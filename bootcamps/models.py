from django.db import models
from django.utils import timezone
from .modelChoices import nationality

level = (
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

applicant_selection = (
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
)

gender = (
    ('Female', 'Female'),
    ('Male', 'Male'),
)

can_code = (
    ('Yes I can code in HTML, CSS & Python', 'Yes I can code in HTML, CSS & Python'),
    ('No I can not code in HTML, CSS & Python', 'No I can not code in HTML, CSS & Python'),
)

training_session = (
    (
        'No Coding Session (Drag and Drop Design)',
        'No Coding Session (Drag and Drop Design)',
    ),
    (
        'Coding Session (Requires basic knowledge of HTML, CSS & Python)',
        'Coding Session (Requires basic knowledge of HTML, CSS & Python)',
    ),
)


class Bootcamp(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=50, choices=gender, default='Female')
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=level, default='Undergrad')
    student_number = models.BigIntegerField(default=1)
    nationality = models.CharField(
        max_length=50,
        choices=nationality,
        default='South Africa',
    )
    phone_number = models.CharField(max_length=30, default='')
    session = models.CharField(
        max_length=100,
        choices=training_session,
        help_text='select training session',
    )
    can_you_code = models.CharField(
        max_length=50,
        choices=can_code,
        default='No',
        null=True,
        blank=True,
        help_text='can you code in HTML, CSS & Python',
    )
    repo_link = models.URLField(
        null=True,
        blank=True,
        help_text='code sample link',
    )
    expectation = models.TextField(max_length=800)
    application_status = models.CharField(
        null=True, blank=True, choices=applicant_selection
    )
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Bootcamp"
        verbose_name_plural = "Bootcamps"
