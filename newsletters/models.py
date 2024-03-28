from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field

from blog.validate_image import clean_image

groups = (
    ('Selected Bootcamp Group', 'Selected Bootcamp Group'),
    ('Rejected Bootcamp Group', 'Rejected Bootcamp Group'),
    ('Newsletter Email Group', 'Newsletter Email Group'),
    ('Bootcamp: Coding Session', 'Bootcamp: Coding Session'),
    ('Bootcamp: Drag and Drop Session', 'Bootcamp: Drag and Drop Session'),
)

groups_followup = (
    ('Selected Bootcamp Group', 'Selected Bootcamp Group'),
    ('Bootcamp: Coding Session', 'Bootcamp: Coding Session'),
    ('Bootcamp: Drag and Drop Session', 'Bootcamp: Drag and Drop Session'),
)


class NewsletterEmail(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
        primary_key=True,
    )
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id


class SendUserEmails(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
        primary_key=True,
    )
    subject = models.CharField(max_length=200)
    group = models.CharField(choices=groups, max_length=100, default="Selected Bootcamp Group")
    salutation = message = CKEditor5Field(
        max_length=5000,
        help_text='to learn more about what format or the style \
                tab content mean kindly click\
                <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element"\
                target="_blank" style="color:wheat;">Here</a>.',
    )
    message = CKEditor5Field(
        max_length=5000,
        help_text='to learn more about what format or the style \
                tab content mean kindly click\
                <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element"\
                target="_blank" style="color:wheat;">Here</a>.',
    )
    link = models.URLField()
    link_title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Send User Email'
        verbose_name_plural = 'Send User Emails'


class SendBootcampReminderEmails(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
        primary_key=True,
    )
    subject = models.CharField(max_length=200)
    group = models.CharField(choices=groups_followup, max_length=100, default="Selected Bootcamp Group")
    main_message_heading = models.CharField(max_length=45, help_text='main heading in email template')
    primary_message_section = CKEditor5Field(max_length=400, help_text='the first message section in the email')
    image_section_heading = models.CharField(max_length=40, help_text='image heading session in email template')
    display_image_1 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    display_image_1_text = models.CharField(max_length=26, help_text='displayed image text for image one')
    display_image_2 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    display_image_2_text = models.CharField(max_length=26, help_text='displayed image text for image two')
    display_image_3 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    display_image_3_text = models.CharField(max_length=26, help_text='displayed image text for image three')
    display_image_4 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    display_image_4_text = models.CharField(max_length=26, help_text='displayed image text for image four')
    secondary_message_section = CKEditor5Field(max_length=400, help_text='the second message section in the email')
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Email Reminder'
        verbose_name_plural = 'Email Reminders'
