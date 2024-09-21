from django.db import models
from django.utils import timezone


class TrainingSettingsBase(models.Model):
    opening_date = models.DateTimeField(default=timezone.now,
                                        help_text='Time registration starts')
    closing_date = models.DateTimeField(default=timezone.now,
                                        help_text='Time registration closes')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bootcamp_title

    class Meta:
        abstract = True


class BootcampSettings(TrainingSettingsBase):
    bootcamp_title = models.CharField(max_length=200)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.bootcamp_title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Bootcamp Settings'
        verbose_name_plural = 'Bootcamp Settings'


class MasterclassSettings(TrainingSettingsBase):
    masterclass_title = models.CharField(max_length=200)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.masterclass_title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Masterclass Settings'
        verbose_name_plural = 'Masterclass Settings'


class ProgramSettings(TrainingSettingsBase):
    event_title = models.CharField(max_length=200)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.event_title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Program Settings'
        verbose_name_plural = 'Program Settings'
