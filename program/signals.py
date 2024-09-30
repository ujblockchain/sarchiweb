from random import randint
from django.core import mail
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from decouple import config
from .models import Program


@receiver(post_save, sender=Program)
def auto_mail_sending(sender, instance, created, **kwargs):
    # avoid sending empty mails
    if (
        created
        or instance.application_status == 'Selected'
        or instance.application_status == 'Rejected'
    ):
        # send email on registration complete
        sender_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = [instance.email]
        email_salutation = 'Thanks,\n UJ Blockchain Team.'

        # email context init
        email_subject = ''
        email_message = ''
        email_link = ''
        email_link_title = ''

        if created:
            # send email on registration complete
            email_subject = 'UJ Blockchain Demo Day'
            email_message = f'Hi {instance.first_name},\n\n\
                Thank you for your interest in attending the UJ Blockchain Demo Day Event, set to take place on October 3rd, 2024. Organized by the SA \
                Swiss Chair in Blockchain Technology at the University of Johannesburg, this event showcases our depth of research and expertise in Blockchain, \
                AI and hardware. \
                Projects ranging from drone designs and computer vision applications to 3D world reconstructions and decentralized solutions used by thousands \
                will be displayed as we showcase our innovations and partnerships across industries since the year began. \n\n\
                Kindly note that your application has been received and is slated for review by our Development Team within 72 hours. \n\n\
                Once again, thank you for applying for the UJ Blockchain Demo Day Event. We are excited and cannot wait to show you some amazing \
                innovations we have been working on 🤩🙌.\
            '
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
                headers={'X-PM-Message-Stream': 'outbound', 'Message-ID': f'{randint(1, 1000)}'},
            )

            # ensure that email format is html
            msg.content_subtype = 'html'

            # attached file
            program_flyer = f'{settings.PROJECT_DIR}/static/images/flyer.png'
            msg.attach_file(program_flyer)

            # send email
            msg.send()
        else:
            # once model is saved, trigger signal
            if instance.application_status == 'Selected':
                email_subject = 'You Have Been Selected 🥳🎉: UJ Blockchain Demo Day'
                email_message = f'Hi {instance.first_name}, \n\n\
                    Thank you for your interest in attending the UJ Blockchain Demo Day Event, set to take place on October 3rd, 2024. Organized by the SA \
                    Swiss Chair in Blockchain Technology at the University of Johannesburg, this event showcases our depth of research and expertise in Blockchain, \
                    AI and hardware. \
                    Projects ranging from drone designs and computer vision applications to 3D world reconstructions and decentralized solutions used by thousands \
                    will be displayed as we showcase our innovations and partnerships across industries since the year began. \n\n\
                    Kindly note that you have been selected to attend the Demo Day event. The event will be held at \
                    <strong style="color: #ff6522 !important;">10 am</strong> on the \
                    <strong style="color: #ff6522 !important;">3rd of October 2024, at the Johannesburg Business School auditorium GLV1 behind the reception</strong>. \n\n\
                    Once again, thank you for applying for the UJ Blockchain Demo Day Event. We are excited and cannot wait to show you some amazing \
                    innovations we have been working on 🤩🙌.\
                '

                email_link = 'https://blockchain.uj.ac.za'
                email_link_title = 'UJ Blockchain'

            elif instance.application_status == 'Rejected':
                email_subject = 'Application Status: UJ Blockchain Demo Day'
                email_message = f'Hi {instance.first_name}, \n\n\
                    Thank you for your interest in attending the UJ Blockchain Demo Day. Unfortunately, you were not selected for the Demo Day event. \
                    We received large applications for the event but could only take a few\n\n\
                    We understand your desire to attend this event and your drive to gain a better perspective on Blockchain and 4IR; yes, \
                    we do. Other events will be coming up; sign up for our newsletter to ensure you register on time. \n\n\
                    Our newsletters give you up-to-date insight into our build stacks and projects we are currently working on. It also gives you the privilege \
                    of getting early registration links for Bootcamps, Hackathon, and other programs like this three days before it is made open to the public. \n\n\
                    Once again, thank you for applying for the UJ Blockchain Demo Day Event. We are excited and cannot wait to see the many frontiers upcoming \
                    events will open for you in your Blockchain Development Journey 🤩🙌.\
                '

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
                headers={'X-PM-Message-Stream': 'outbound', 'Message-ID': f'{randint(1, 1000)}'},
            )

            # ensure that email format is html
            msg.content_subtype = 'html'

            # attached file
            if instance.application_status == 'Selected':
                program_flyer = f'{settings.PROJECT_DIR}/static/images/flyer.png'
                msg.attach_file(program_flyer)

            # send email
            msg.send()
