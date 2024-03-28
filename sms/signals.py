from django.dispatch import receiver
from django.db.models.signals import post_save
from bootcamps.models import Bootcamp
from sms.utils.iso_time import isoformat
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
                training_session='Coding Session (Requires basic knowledge of HTML, CSS & Python)').values_list(
                    'phone_number', flat=True)
        # for those selected in the drag and drop sessions
        elif group == 'Bootcamp: Drag and Drop Session':
            # get the email list
            sms_list = Bootcamp.objects.filter(
                training_session='No Coding Session (Drag and Drop Design)').values_list('phone_number', flat=True)

        # init number of  elements each list should have
        n = 15  # 15 per list

        # using list comprehension to split sms list into multiple lists in a single list
        sorted_sms_list = [sms_list[i:i + n] for i in range(0, len(sms_list), n)]

        # message delivery time in ISO 8601
        sms_delivery_time = isoformat(instance.schedule_message)

        # init task
        send_sms_task(sorted_sms_list, instance.message, sms_delivery_time)
