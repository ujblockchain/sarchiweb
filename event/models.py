from django.db import models
from django.utils import timezone

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

EVENT_CHOICES = [
    ('ujb', 'UJ Blockchain Event'),
    ('fews', 'CCFEWS Event'),
]


class EventEmailConfig(models.Model):
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    applied_subject = models.CharField(max_length=255, default="Application Received")
    applied_message_text = models.TextField(
        verbose_name="Applied Message (Single)",
        help_text="Used when saving a single record. Use HTML like &lt;br&gt; or &lt;strong&gt;. \
            Use variables like {{ first_name }}, {{ last_name }}, {{ organization }}.",
    )

    selected_subject = models.CharField(max_length=255, default="You are Selected")
    selected_message_text = models.TextField(
        verbose_name="Selected Message (Single)",
        help_text="Used when saving a single record. Use HTML like &lt;br&gt; or &lt;strong&gt;. \
            Use variables like {{ first_name }}, {{ last_name }}, {{ organization }}.",
    )
    selected_bulk_message_text = models.TextField(
        verbose_name="Selected Message (Bulk)",
        help_text="Used when updating multiple records via Admin Actions. Do not use personal variables here. \
            Start with a generic greeting like 'Hi there,' or 'Dear Applicant,'.",
    )
    rejected_subject = models.CharField(max_length=255, default="Application Update")
    rejected_message_text = models.TextField(
        verbose_name="Rejected Message (Single)",
        help_text="Used when saving a single record. Use HTML like &lt;br&gt; or &lt;strong&gt;. \
            Use variables like {{ first_name }}, {{ last_name }}, {{ organization }}.",
    )
    rejected_bulk_message_text = models.TextField(
        verbose_name="Rejected Message (Bulk)",
        help_text="Used when updating multiple records via Admin Actions. Do not use personal variables here. \
            Start with a generic greeting like 'Hi there,' or 'Dear Applicant,'.",
    )
    group_link = models.URLField(
        blank=True,
        null=True,
        help_text="Optional link for groups (e.g., LinkedIn/WhatsApp).",
    )
    attachment = models.FileField(
        upload_to='email_flyers/',
        blank=True,
        null=True,
        help_text="Optional flyer or document to attach.",
    )
    registration_end_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Email Configuration"
        verbose_name_plural = "Email Configurations"

    def __str__(self):
        return f"{self.event_type.upper()} Email Template"


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
    email = models.EmailField(help_text="User's email address")
    phone = models.CharField(max_length=20)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=50, default='FEWS', null=True, blank=True, editable=False)
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
    event_type = models.CharField(max_length=50, default='UJB', null=True, blank=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "FEWS Registration"
        verbose_name_plural = "FEWS Registrations"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.organization}"
