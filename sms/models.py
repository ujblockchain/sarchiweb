from datetime import datetime
from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField

groups = (
    ('Selected Bootcamp Group', 'Selected Bootcamp Group'),
    ('Bootcamp: Coding Session', 'Bootcamp: Coding Session'),
    ('Bootcamp: Drag and Drop Session', 'Bootcamp: Drag and Drop Session'),
)


class SendUserSms(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet='abcdefg1234',
        primary_key=True,
    )
    title = models.CharField(max_length=200, help_text='title is not used in sms')
    group = models.CharField(choices=groups, max_length=100, default='select bootcamp group')
    message = models.TextField(
        max_length=151,
        help_text='sms message',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Send SMS To User'
        verbose_name_plural = 'Send SMS To Users'
