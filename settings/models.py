from django.db import models
from django.utils import timezone
from blog.validate_image import clean_image

link_action = [('Internal', 'Internal'), ('External', 'External')]


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


class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    event_info = models.TextField(max_length=240)
    event_date = models.DateTimeField()
    image = models.ImageField(upload_to='event/flyer',
                              validators=[clean_image])
    link_type = models.CharField(choices=link_action, default='Internal')
    registration_link = models.URLField(default='https://blockchain.uj.ac.za')
    event_website = models.URLField(default='https://blockchain.uj.ac.za')
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_update']
        verbose_name = 'Upcoming Event'
        verbose_name_plural = 'Upcoming Events'
