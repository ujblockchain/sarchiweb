from random import randint

from decouple import config
from django.conf import settings
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders

from .models import ProgramSignUp


@receiver(post_save, sender=ProgramSignUp)
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
        email_salutation = 'Thanks,\n\n UJ Blockchain Team.'

        # email context init
        email_subject = ''
        email_message = ''
        email_link = ''
        email_link_title = ''
        application_status = instance.application_status

        if created:
            # send email on registration complete
            email_subject = (
                'BACISS (Blockchain · AI · Cloud · Innovation · Startup School)'
            )
            email_message = f'Hi {instance.first_name},\n\n\
                Thank you for your interest in attending BACISS (Blockchain · AI · Cloud · Innovation · Startup School), \
                an immersive, hands-on innovation program designed to empower students, researchers, and entrepreneurs \
                to build, innovate, and scale technology-driven ventures. The event is set to take \
                place on 17th-21st November 2025. Organized by the South Africa - \
                Switzerland Chair in Blockchain Technology at the University of Johannesburg in \
                collaboration with industry partners, this event \
                aims build, innovate, and scale technology-driven ventures. \n\n\
                Kindly note that your application has been received and is slated for review \
                by our Development Team. \n\n\
                Once again, thank you for applying for the BACISS Event. \
                We are excited and cannot wait to see the amazing \
                innovations you will build 🤩🙌.\
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
                    'application_status': application_status,
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
            # program_flyer = finders.find('images/flyer.jpg')
            # print(program_flyer)
            # msg.attach_file(program_flyer)

            # send email
            msg.send(fail_silently=True)

        else:
            # once model is saved, trigger signal
            if instance.application_status == 'Selected':
                email_subject = 'You Have Been Selected 🥳🎉: BACISS (Blockchain · AI · Cloud · Innovation · Startup School)'
                email_message = f'Hi {instance.first_name}, \n\n\
                    Thank you for your interest in attending BACISS (Blockchain · AI · Cloud · Innovation · Startup School), \
                    an immersive, hands-on innovation program designed to empower students, researchers, and entrepreneurs \
                    to build, innovate, and scale technology-driven ventures. The event is set to take \
                    place on 17th-21st November 2025. Organized by the South Africa - \
                    Switzerland Chair in Blockchain Technology at the University of Johannesburg in \
                    collaboration with industry partners,  this event \
                    aims build, innovate, and scale technology-driven ventures. \n\n\
                    Kindly note that you have been selected to attend this event \
                    The event will be held at \
                    <strong style="color: #ff6522 !important;">9 am daily</strong> on the \
                    <strong style="color: #ff6522 !important;">17th-21st November 2025, at \
                    B2 Lab 219, Department of Electrical Electronics, Engineering Building, \
                    Kingsway Campus (APK Campus), University of Johannesburg. \n\n\
                    Once again, thank you for applying for the BACISS Event. \
                    We are excited and cannot wait to see the amazing \
                    innovations you will build 🤩🙌.\
                '

                email_link = 'https://blockchain.uj.ac.za'
                email_link_title = 'UJ Blockchain'

            elif instance.application_status == 'Rejected':
                email_subject = 'Application Status: BACISS (Blockchain · AI · Cloud · Innovation · Startup School)'
                email_message = f'Hi {instance.first_name}, \n\n\
                    Thank you for your interest in attending the BACISS (Blockchain · AI · Cloud · Innovation · Startup School) event. \
                    Unfortunately, you were not selected for the event. \
                    We received large applications for the event but could only take a few\n\n\
                    We understand your desire to attend this event and your drive to gain a \
                    better perspective on building startup solutions; yes, \
                    we do. Other events like this will be coming up; sign up for our newsletter to ensure \
                    you register on time. \n\n\
                    Our newsletters give you up-to-date insight into our build stacks and projects \
                    we are currently working on. It also gives you the privilege \
                    of getting early registration links for Bootcamps, Hackathon, and other programs \
                    like this three days before it is made open to the public. \n\n\
                    Once again, thank you for applying for the BACISS (Blockchain · AI · Cloud · Innovation · Startup School) Event. \
                    We are excited and cannot wait to see the many frontiers upcoming \
                    events will open for you in your startup Journey 🤩🙌.\
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
                    'application_status': application_status,
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
            # if instance.application_status == 'Selected':
            #     program_flyer = finders.find('images/flyer.jpg')
            #     msg.attach_file(program_flyer)

            # send email
            msg.send(fail_silently=True)
