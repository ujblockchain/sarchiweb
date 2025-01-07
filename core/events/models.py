from django.db import models
from django.utils import timezone

from core.blog.utils.validate_image import clean_image

# model choices
link_action = [('Internal', 'Internal'), ('External', 'External')]


class EventBase(models.Model):
    opening_date = models.DateTimeField(default=timezone.now, help_text='Time registration starts')
    closing_date = models.DateTimeField(default=timezone.now, help_text='Time registration closes')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bootcamp_title

    class Meta:
        abstract = True


class Event(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField(max_length=240, help_text='event description')
    date = models.DateTimeField(help_text='date event starts')
    image = models.ImageField(upload_to='event/flyer', validators=[clean_image], help_text='event flyer or poster')
    link_type = models.CharField(choices=link_action, default='Internal')
    registration_link = models.URLField(default='https://blockchain.uj.ac.za')
    website = models.URLField(default='https://blockchain.uj.ac.za', help_text='link to event website')
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_update']
        verbose_name = 'Event Ads'
        verbose_name_plural = 'Event Ads'
