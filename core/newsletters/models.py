from django.db import models
from django.utils import timezone
from django_prose_editor.fields import ProseEditorField
from shortuuid.django_fields import ShortUUIDField

from core.blog.utils.validate_image import clean_image

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
    id = ShortUUIDField(length=16, max_length=40, alphabet='abcdefg1234', primary_key=True)  # noqa: A003
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['-date_created']


class SendUserEmails(models.Model):
    id = ShortUUIDField(length=16, max_length=40, alphabet='abcdefg1234', primary_key=True)  # noqa: A003
    subject = models.CharField(max_length=200)
    group = models.CharField(choices=groups, max_length=100, default='Selected Bootcamp Group')
    salutation_message = ProseEditorField(
        max_length=5000,
        help_text='to learn more about what format or the style \
                tab content mean kindly click\
                <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Element"\
                target="_blank" style="color:wheat;">Here</a>.'
    )
    message = ProseEditorField(
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
    id = ShortUUIDField(length=16, max_length=40, alphabet='abcdefg1234', primary_key=True)  # noqa: A003
    subject = models.CharField(max_length=200)
    group = models.CharField(choices=groups_followup, max_length=100, default='Selected Bootcamp Group')
    main_message_heading = models.CharField(max_length=45, help_text='main heading in email template')
    primary_message_section = ProseEditorField(max_length=650, help_text='the first message section in the email')
    image_section_heading = models.CharField(
        max_length=40, null=True, blank=True, help_text='image heading session in email template'
    )
    gallery_image_1 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    gallery_image_1_text = models.CharField(max_length=26, help_text='gallery image text for image one')
    gallery_image_2 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    gallery_image_2_text = models.CharField(max_length=26, help_text='gallery image text for image two')
    gallery_image_3 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    gallery_image_3_text = models.CharField(max_length=26, help_text='gallery image text for image three')
    gallery_image_4 = models.ImageField(upload_to='email/template/', validators=[clean_image])
    gallery_image_4_text = models.CharField(max_length=26, help_text='displayed image text for image four')
    secondary_message_section = ProseEditorField(max_length=650, help_text='the second message section in the email')
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Email Reminder'
        verbose_name_plural = 'Email Reminders'
