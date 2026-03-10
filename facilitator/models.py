from django.db import models

from contact.models import generate_custom_id

YEAR_CHOICES = [
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
]


class StudentApplication(models.Model):
    id = models.CharField(
        default=generate_custom_id,
        editable=False,
        unique=True,
        max_length=20,
        primary_key=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        error_messages={'unique': "An application with this email already exists."},
    )
    phone_number = models.CharField(max_length=20)
    faculty = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    nationality = models.CharField(max_length=100)
    year_of_study = models.IntegerField(choices=YEAR_CHOICES)
    ieee_membership = models.BooleanField(default=False)
    saiee_membership = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
