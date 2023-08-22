from django.db import models
from django.utils import timezone


class UserContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField(max_length=800)
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-date_created']
        verbose_name = "User Message"
        verbose_name_plural = "User Massages"
