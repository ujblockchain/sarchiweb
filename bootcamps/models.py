from django.db import models
from django.utils import timezone
from .modelChoices import nationality

level = (
    ('Higher Certificate', 'Higher Certificate'),
    ('Diploma', 'Diploma'),
    ('Honours', 'Honours'),
    ('Undergrad', 'Undergrad'),
    ('Post Graduate', 'Post Graduate'),
    ('Others', 'Others'),
)

applicant_selection = (
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
)


class BootcampFirst(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=level, default='Undergrad')
    nationality = models.CharField(max_length=50, choices=nationality, default='South Africa')
    expectation = models.TextField(max_length=800)
    application_status = models.CharField(null=True, blank=True, choices=applicant_selection)
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Bootcamp Sep 2023"
        verbose_name_plural = "Bootcamp Sep 2023"
