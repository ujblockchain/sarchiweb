from random import randint
from django.core import mail
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from decouple import config
from .models import NewsletterEmail, SendNewsletterEmails
from bootcamps.models import BootcampFirst


@receiver(post_save, sender=SendNewsletterEmails)
def auto_mail_sending(sender, instance, created, **kwargs):
    # send emails once, only on create
    if created:
        # init receiver email
        receiver_emails = ""

        # use value_list to get use emails based on selection groups
        ## for those selected for bootcamps
        if instance.group == 'Selected Bootcamp Group':
            receiver_emails = BootcampFirst.objects.filter(
                application_status='Selected'
            ).values_list('email', flat=True)
        ## for those not selected for bootcamps
        elif instance.group == 'Rejected Bootcamp Group':
            receiver_emails = BootcampFirst.objects.filter(
                application_status='Rejected'
            ).values_list('email', flat=True)
        ## for for news letter Signup
        elif instance.group == 'Newsletter Email Group':
            receiver_emails = NewsletterEmail.objects.all().values_list('email', flat=True)

        #init email details
        sender_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = receiver_emails
        email_salutation = instance.salutation
        email_subject = instance.subject
        email_message = instance.message
        email_link = instance.link
        email_link_title = instance.link_title

        # use email template
        html_content = render_to_string(
            'email/email.html',
            {  # pass context to email template
                'email_subject': email_subject,
                'email_message': email_message,
                'email_link': email_link,
                'email_link_title': email_link_title,
                'email_salutation': email_salutation,
            },
        )

        # create HTML email.
        msg = mail.EmailMessage(
            email_subject,
            html_content,
            sender_email,
            recipient_email,
            reply_to=[config('ADMIN_REPLY_EMAIL')],
            headers={'X-PM-Message-Stream': 'outbound', 'Message-ID': f'{randint(1, 1000)}'},
        )

        # ensure that email format is html
        msg.content_subtype = 'html'

        # attached file
        bootcamp_flyer = f'{settings.PROJECT_DIR}/static/images/bootcamp.jpg'
        msg.attach_file(bootcamp_flyer)

        # send email
        msg.send()
