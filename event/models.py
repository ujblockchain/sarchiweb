from django.db import models

from contact.models import generate_custom_id

YEAR_CHOICES = [
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year / Advanced Diploma'),
    ('postgrad', 'Postgraduate'),
]

STATUS_CHOICES = [
    ('selected', 'Selected'),
    ('rejected', 'Rejected'),
]

ATTENDANCE_CHOICES = [
    ('in-person', 'In-Person'),
    ('online', 'YouTube Live'),
]


class EventRegistration(models.Model):
    id = models.CharField(
        default=generate_custom_id,
        editable=False,
        unique=True,
        max_length=20,
        primary_key=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, help_text="User's email address")
    phone = models.CharField(max_length=20)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class FewsRegistration(models.Model):

    id = models.CharField(
        default=generate_custom_id,
        editable=False,
        unique=True,
        max_length=20,
        primary_key=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(
        max_length=255, verbose_name="Institution / Organization"
    )
    attendance_type = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "FEWS Registration"
        verbose_name_plural = "FEWS Registrations"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.organization}"
