from django.db import models
from django.utils import timezone


class BootcampSettings(models.Model):
    bootcamp_title = models.CharField(max_length=200)
    opening_date = models.DateTimeField(default=timezone.now, help_text='Time registration starts')
    closing_date = models.DateTimeField(help_text='Time registration closes')
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.bootcamp_title

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Bootcamp Settings"
        verbose_name_plural = "Bootcamp Settings"
