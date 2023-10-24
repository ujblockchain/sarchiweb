from django.db import models
from django.utils import timezone
from blog.validate_image import clean_image
from bootcamps.modelChoices import nationality

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


class Program(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=50, choices=gender, default='Female')
    nationality = models.CharField(max_length=50, choices=nationality, default='South Africa')
    phone_number = models.CharField(max_length=30, default='')
    organization = models.CharField(max_length=300, default='University of Johannesburg')
    expectation = models.TextField(max_length=800)
    application_status = models.CharField(null=True, blank=True, choices=applicant_selection)
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Program"
        verbose_name_plural = "Program"


class Event(models.Model):
    title = models.CharField(max_length=400)
    speakers = models.CharField(max_length=300)
    speaker_one  = models.ImageField(upload_to='event/speakers/', null=True, blank=True, validators=[clean_image])
    speaker_two  = models.ImageField(upload_to='event/speakers/', null=True, blank=True, validators=[clean_image])
    speaker_three  = models.ImageField(upload_to='event/speakers/', null=True, blank=True, validators=[clean_image])
    speaker_four  = models.ImageField(upload_to='event/speakers/', null=True, blank=True, validators=[clean_image])
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Event Feed"
        verbose_name_plural = "Event Feed"
