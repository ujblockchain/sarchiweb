from django.db.models.signals import post_save
from django.dispatch import receiver
from event.utils import send_single_status_email
from .models import EventRegistration, FewsRegistration


@receiver(post_save, sender=EventRegistration)
def auto_mail_sending(sender, instance, created, **kwargs):

    if created:
        send_single_status_email(instance, status='applied')


@receiver(post_save, sender=FewsRegistration)
def fews_mail_sending(sender, instance, created, **kwargs):
    if created:
        send_single_status_email(instance, status='applied')
