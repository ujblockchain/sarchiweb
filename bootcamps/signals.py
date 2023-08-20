from random import randint
from django.core import mail
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.db.models.signals import pre_save, post_save
from decouple import config
from .models import BootcampFirst


@receiver(post_save, sender=BootcampFirst)
def auto_mail_sending(sender, instance, created, **kwargs):
    # once model is saved, trigger signal
    if created:
        # send email on registration complete
        recipient_email = [instance.email]
        email_subject = 'Demystifying Blockchain Bootcamp'
        sender_email = settings.DEFAULT_FROM_EMAIL
        email_message = f'Hi {instance.first_name},\n\nThank you for your interest and consequent application to the Demystifying Blockchain Bootcamp. \n\nYour interest in coding and desire to upskill aligns with our vision of building practical capacity in blockchain.\n\n. We have received your application, which is slated for review by our development team. \n\n Due to the large volume of applications we have received so far, this process will take a couple of days but be assured that we will be in contact every step of the way.\n\n While you wait, kindly connect with us via our website; you can also access our open-source repository (github.com/ujblockchain) for code guides and tips.\n\nOnce again, thank you for applying for the Demystifying Blockchain Bootcamp. We are excited and cannot wait to begin this fantastic journey of Blockchain development, step by step, with You!'
        email_salutation = 'Thanks,\n UJ Blockchain Team.'
        email_link = 'https://blockchain.uj.ac.za'
        email_link_title = 'UJ Blockchain'

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
            headers={'Message-ID': f'{randint(1, 1000)}'},
        )

        # ensure that email format is html
        msg.content_subtype = 'html'
        # send email
        msg.send()


# trigger signal once applicants are selected
@receiver(pre_save, sender=BootcampFirst)
def auto_selection_mail_sending(sender, instance, **kwargs):
    # once model is saved, trigger signal
    if instance.application_status == "Selected":
        # send email on registration complete
        recipient_email = [instance.email]
        email_subject = 'You Have Been Selected 🥳🎉: Demystifying Blockchain Bootcamp'
        sender_email = settings.DEFAULT_FROM_EMAIL
        email_message = f'Hi {instance.first_name},\n\nThank you for your interest and consequent application to the Demystifying Blockchain Bootcamp. \n\nYour interest in coding and desire to upskill aligns with our vision of building practical capacity in blockchain.\n\n. We are glad to inform you that you have been selected for the Demystifying Blockchain Bootcamp. In this training, you will be taken step by step from beginning to knowing and coding in blockchain.\n\n You are only to come with your computer; the rest will be provided, including tea breaks and lunch for every training day. We will also offer coding support during and after the Bootcamp.\n\nOnce again, on behalf of our entire team, a big congratulations. We are excited and ready to begin this fantastic journey of Blockchain development, step by step, with You!🤩🙌.'
        email_salutation = 'Thanks,\n UJ Blockchain Team.'
        email_link = 'https://blockchain.uj.ac.za'
        email_link_title = 'UJ Blockchain'

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
            headers={'Message-ID': f'{randint(1, 1000)}'},
        )

        # ensure that email format is html
        msg.content_subtype = 'html'
        # send email
        msg.send()
