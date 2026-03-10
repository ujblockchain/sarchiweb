from django.db import models

from contact.models import generate_custom_id

YEAR_CHOICES = [
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year / Advanced Diploma'),
    ('postgrad', 'Postgraduate'),
]


class CommunityRegistration(models.Model):
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
