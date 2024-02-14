from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field

groups = (
    ('Selected Bootcamp Group', 'Selected Bootcamp Group'),
    ('Rejected Bootcamp Group', 'Rejected Bootcamp Group'),
    ('Newsletter Email Group', 'Newsletter Email Group'),
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


class SendNewsletterEmails(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
        primary_key=True,
    )
    subject = models.CharField(max_length=200)
    group = models.CharField(
        choices=groups, max_length=100, default="Selected Bootcamp Group"
    )
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
        verbose_name = 'Send Email'
        verbose_name_plural = 'Send Emails'
