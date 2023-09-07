from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField


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
