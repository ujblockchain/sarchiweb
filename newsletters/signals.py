from django.dispatch import receiver
from django.db.models.signals import post_save
from bootcamps.models import Bootcamp
from .models import NewsletterEmail, SendUserEmails, SendBootcampReminderEmails
#
from .tasks import reminder_email_task, send_email_task


@receiver(post_save, sender=SendUserEmails)
def auto_mail_sending(sender, instance, created, **kwargs):
    # send emails once, only on create
    if created:
        # init receiver email list
        email_list = ''
        group = instance.group

        # use value_list to get use emails based on selection groups
        ## for those selected for bootcamp
        if group == 'Selected Bootcamp Group':
            # get the email list
            email_list = Bootcamp.objects.filter(application_status='Selected').values_list('email', flat=True)

        ## for those not selected for bootcamps
        elif group == 'Rejected Bootcamp Group':
            # get the email list
            email_list = Bootcamp.objects.filter(application_status='Rejected').values_list('email', flat=True)

        # for those in coding session for bootcamps
        elif group == 'Bootcamp: Coding Session':
            # get the email list
            email_list = Bootcamp.objects.filter(
                training_session='Coding Session (Requires basic knowledge of HTML, CSS & Python)').values_list(
                    'email', flat=True)

        # for those in drag and drop session for bootcamps
        elif group == 'Bootcamp: Drag and Drop Session':
            # get the email list
            email_list = Bootcamp.objects.filter(
                training_session='No Coding Session (Drag and Drop Design)').values_list('email', flat=True)

        ## for newsletter Signup
        elif group == 'Newsletter Email Group':
            # get the email list
            email_list = NewsletterEmail.objects.all().values_list('email', flat=True)

        # init number of  elements each list should have
        n = 15  # 15 per list

        # using list comprehension to split email list into multiple lists in a single list
        sorted_email_list = [email_list[i:i + n] for i in range(0, len(email_list), n)]

        # init task
        send_email_task(sorted_email_list, instance.salutation, instance.subject, instance.message, instance.link,
                        instance.link_title)


@receiver(post_save, sender=SendBootcampReminderEmails)
def auto_mail_reminder_sending(sender, instance, created, **kwargs):
    # send emails once, only on create
    if created:
        # init receiver email list
        email_list = ''
        group = instance.group

        # use value_list to get use emails based on selection groups
        ## for those selected for bootcamp
        if group == 'Selected Bootcamp Group':
            # get the email list
            email_list = Bootcamp.objects.filter(application_status='Selected').values_list('email', flat=True)

        # for those in coding session for bootcamps
        elif group == 'Bootcamp: Coding Session':
            # get the email list
            email_list = Bootcamp.objects.filter(
                training_session='Coding Session (Requires basic knowledge of HTML, CSS & Python)').values_list(
                    'email', flat=True)

        # for those in drag and drop session for bootcamps
        elif group == 'Bootcamp: Drag and Drop Session':
            # get the email list
            email_list = Bootcamp.objects.filter(
                training_session='No Coding Session (Drag and Drop Design)').values_list('email', flat=True)

        # init number of  elements each list should have
        n = 15  # 15 per list

        # using list comprehension to split email list into multiple lists in a single list
        sorted_email_list = [email_list[i:i + n] for i in range(0, len(email_list), n)]

        #format images
        image_1 = f'https://www.blockchain.uj.ac.za/media/{instance.display_image_1}'
        image_2 = f'https://www.blockchain.uj.ac.za/media/{instance.display_image_2}'
        image_3 = f'https://www.blockchain.uj.ac.za/media/{instance.display_image_3}'
        image_4 = f'https://www.blockchain.uj.ac.za/media/{instance.display_image_4}'

        # init task
        reminder_email_task(sorted_email_list, instance.subject, instance.main_message_heading,
                            instance.primary_message_section, instance.image_section_heading, image_1,
                            instance.display_image_1_text, image_2, instance.display_image_2_text, image_3,
                            instance.display_image_3_text, image_4, instance.display_image_4_text,
                            instance.secondary_message_section)
