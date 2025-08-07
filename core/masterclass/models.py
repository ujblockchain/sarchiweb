from django.db import models
from django.utils import timezone

from core.bootcamps.models import TrainingBaseModel
from core.events.models import EventBase


class MasterclassConfig(EventBase):
    masterclass_title = models.CharField(max_length=200)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.masterclass_title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Masterclass Config'
        verbose_name_plural = 'Masterclass Configs'


class Masterclass(TrainingBaseModel):
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Masterclass'
        verbose_name_plural = 'Masterclass'
