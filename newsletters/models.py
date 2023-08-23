from django.db import models
from django.utils import timezone


class NewsletterEmail(models.Model):
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)
