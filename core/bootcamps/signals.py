from random import randint

from decouple import config
from django.conf import settings
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import BootcampSignup


@receiver(post_save, sender=BootcampSignup)
def auto_mail_sending(sender, instance, created, **kwargs):
    # avoid sending empty mails
    if (created or instance.application_status == 'Selected' or instance.application_status == 'Rejected'):

        # send email on registration complete
        sender_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = [instance.email]
        email_salutation = 'Thanks, <br /> UJ Blockchain Team.'

        # email context init
        email_subject = ''
        email_message = ''
        email_link = ''
        email_link_title = ''

        if created:
            # send email on registration complete
            email_subject = 'Demystifying Blockchain Bootcamp'
            email_message = f'Hi {instance.first_name};\n\nThank you for your interest and consequent \
                application to the Demystifying Blockchain Bootcamp coming up at <strong>April 2nd - \
                5th 2024 at the School of Tourism and Hospitality (STH), APB Campus, University of \
                Johannesburg</strong>. \n\nYour interest in coding and desire to upskill aligns with \
                our vision of building practical capacity in blockchain.\n\n We have received your \
                application, which is slated for review by our development team. Due to the large \
                volume of applications we have received so far, this process will take a couple of \
                days but be assured that we will be in contact every step of the way. \n\n While you \
                wait, kindly connect with us via our <a href="http://blockchain.uj.ac.za" target="_blank" \
                style="color: #ff6522 !important;">website</a>; you can also access our open-source repository \
                (<a href="http://github.com/ujblockchain" target="_blank" style="color: #ff6522 !important;">\
                github.com/ujblockchain</a>) and YouTube Channel (<a href="https://www.youtube.com/@ujblockchain" \
                target="_blank" style="color: #ff6522 !important;">youtube.com/@ujblockchain</a>) for code guides, \
                tips and video tutorials.\n\nOnce again, thank you for applying for the Demystifying \
                Blockchain Bootcamp. We are excited and cannot wait to begin this fantastic journey of \
                Blockchain development, step by step, with You!'

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
                headers={
                    'X-PM-Message-Stream': 'outbound',
                    'Message-ID': f'{randint(1, 1000)}',
                },
            )

            # ensure that email format is html
            msg.content_subtype = 'html'

            # attached file
            bootcamp_flyer = f'{settings.PROJECT_DIR}/static/images/Bootcamp.png'
            msg.attach_file(bootcamp_flyer)

            # send email
            msg.send()

        elif (instance.application_status == 'Selected' or instance.application_status == 'Rejected'):
            # once model is saved, trigger signal
            if instance.application_status == 'Selected':
                email_subject = ('You Have Been Selected 🥳🎉: Demystifying Blockchain Bootcamp')
                email_message = f'Hi {instance.first_name};\n\nThank you for your interest and \
                    consequent application to the Demystifying Blockchain Bootcamp coming up by \
                    <strong>April 2nd - 5th 2024 at the School of Tourism and Hospitality (STH), \
                    APB Campus, University of Johannesburg</strong>. \n\nYour interest in coding \
                    and desire to upskill aligns with our vision of building practical capacity in \
                    blockchain. We are glad to inform you that you have been selected for the \
                    Demystifying Blockchain Bootcamp. In this training, you will be taken step \
                    by step from beginning to knowing and coding in blockchain.\n\n The venue for \
                    this training is <strong>School of Tourism and Hospitality (STH), APB Campus, \
                    University of Johannesburg, with free transportation provided from APK campus \
                    Gate 2 every day of the training from 7am each day of the training</strong>. \
                    You are only to come with your computer; the rest will be provided, including \
                    tea breaks and lunch for every training day. We will also offer coding support \
                    during and after the Bootcamp.\n\nOnce again, on behalf of our entire team, a \
                    big congratulations. We are excited and ready to begin this fantastic journey \
                    of Blockchain development, step by step, with You!🤩🙌.'

                email_link = 'https://blockchain.uj.ac.za'
                email_link_title = 'UJ Blockchain'
            elif instance.application_status == 'Rejected':
                email_subject = 'Application Status: Demystifying Blockchain Bootcamp'
                email_message = f'Hi {instance.first_name};\n\nThank you for your interest and \
                    consequent application to the Demystifying Blockchain Bootcamp. \
                    \n\nYour interest in coding and desire to upskill aligns with our vision \
                    of building practical capacity in blockchain.\n\n Unfortunately, you were \
                    not selected for the Bootcamp. We received large volumes of applications \
                    for the training, but we could only take a few for the Bootcamp. \n\n We \
                    understand your desire to attend the Bootcamp and your drive to upskill in \
                    Blockchain; yes, we do. There will be other Bootcamp, Hackathon, Media Events \
                    and Project Demo coming up starting from May 2024. We will be having the next \
                    bootcamp come September 2024; this Bootcamp also comes with a hands-on where you will \
                    be taught step by step by our development team.\n\n To ensure you register in time, \
                    sign up for our newsletter. Our newsletters gives you up-to-date insight into our \
                    build stacks and projects we are currently working on. It also gives you the privilege of \
                    getting early registration links for Bootcamps, Hackathon, and other programs three \
                    days before it is made open to the general public. You can also follow us on our social \
                    media handles and checkout our open-source repository \
                    (<a href="http://github.com/ujblockchain" target="_blank" \
                    style="color: #ff6522 !important;">github.com/ujblockchain</a>) \
                    and YouTube Channel \
                    (<a href="https://www.youtube.com/@ujblockchain" target="_blank" \
                    style="color: #ff6522 !important;">youtube.com/@ujblockchain</a>) \
                    for code guides, tips and video tutorials.\n\n We are excited and look forward to \
                    seeing you in our future Bootcamps and Hackathon as we hope to begin a  fantastic \
                    journey of Blockchain development, step by step, with You!🤩🙌.'

                email_link = 'https://blockchain.uj.ac.za/#newsletter'
                email_link_title = 'Newsletter'

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
                headers={
                    'X-PM-Message-Stream': 'outbound',
                    'Message-ID': f'{randint(1, 1000)}',
                },
            )

            # ensure that email format is html
            msg.content_subtype = 'html'

            # attached file
            if instance.application_status == 'Selected':
                bootcamp_flyer = f'{settings.PROJECT_DIR}/static/images/Bootcamp.png'
                msg.attach_file(bootcamp_flyer)

            # send email
            msg.send()
