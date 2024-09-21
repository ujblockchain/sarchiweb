from django.db import models
from django.utils import timezone
from bootcamps.models import TrainingBaseModel
from settings.models import MasterclassSettings


class Masterclass(TrainingBaseModel):
    masterclass_settings = models.ForeignKey(
        MasterclassSettings,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Masterclass'
        verbose_name_plural = 'Masterclass'
