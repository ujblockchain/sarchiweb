from django.dispatch import receiver
from django.db.models.signals import post_save
from bootcamps.models import Bootcamp
from .models import SendUserSms
#
from .tasks import send_sms_task


@receiver(post_save, sender=SendUserSms)
def auto_sms_sending(sender, instance, created, **kwargs):
    # send sms once, only on create
    if created:
        # init receiver sms list
        sms_list = ''
        group = instance.group

        # use value_list to get user phone number based on selection groups
        # for all selected for bootcamp
        if group == 'Selected Bootcamp Group':
            # get the phone number list
            sms_list = Bootcamp.objects.filter(application_status='Selected').values_list('phone_number', flat=True)
        # for those selected in the coding sessions
        elif group == 'Bootcamp: Coding Session':
            # get the  phone number list
            sms_list = Bootcamp.objects.filter(
                session='Coding Session (Requires basic knowledge of HTML, CSS & Python)',
                application_status='Selected').values_list('phone_number', flat=True)
        # for those selected in the drag and drop sessions
        elif group == 'Bootcamp: Drag and Drop Session':
            # get the email list
            sms_list = Bootcamp.objects.filter(session='No Coding Session (Drag and Drop Design)',
                                               application_status='Selected').values_list('phone_number', flat=True)

        # init task
        send_sms_task(sms_list, instance.message)
