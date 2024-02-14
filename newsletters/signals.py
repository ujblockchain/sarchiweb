from django.dispatch import receiver
from django.db.models.signals import post_save
from bootcamps.models import Bootcamp
from .models import NewsletterEmail, SendNewsletterEmails

from .tasks import send_email_task


@receiver(post_save, sender=SendNewsletterEmails)
def auto_mail_sending(sender, instance, created, **kwargs):
    # send emails once, only on create
    if created:
        # init receiver email list
        email_list = ""
        group = instance.group

        # use value_list to get use emails based on selection groups
        ## for those selected for bootcamp
        if group == 'Selected Bootcamp Group':
            # get the email list
            email_list = Bootcamp.objects.filter(
                application_status='Selected'
            ).values_list('email', flat=True)

        ## for those not selected for bootcamps
        elif group == 'Rejected Bootcamp Group':
            # get the email list
            email_list = Bootcamp.objects.filter(
                application_status='Rejected'
            ).values_list('email', flat=True)
        ## for for news letter Signup
        elif group == 'Newsletter Email Group':
            # get the email list
            email_list = NewsletterEmail.objects.all().values_list('email', flat=True)

        # init number of  elements each list should have
        n = 15  # 15 per list

        # using list comprehension to split email list into multiple lists
        sorted_email_list = [
            email_list[i : i + n] for i in range(0, len(email_list), n)
        ]

        # init task
        send_email_task(
            sorted_email_list,
            instance.salutation,
            instance.subject,
            instance.message,
            instance.link,
            instance.link_title,
        )
