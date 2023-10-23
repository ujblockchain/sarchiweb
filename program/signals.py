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
            email_subject = 'Mainstreaming Blockchain (MB)'
            email_message = f'Hi {instance.first_name},\n\n\
                Thank you for your interest and for submitting your application to attend the Mainstreaming Blockchain (MB): \
                A Thought Leadership Media Event. Mainstreaming Blockchain is set to take place on October 24, 2023. Organized by \
                the SA/Swiss Chair on Blockchain Technology at the University of Johannesburg, this event will bring together blockchain \
                enthusiasts, industry experts, researchers, and thought leaders. Its primary focus is to delve into the immense potential \
                of blockchain technology in South and Sub-Saharan Africa. \n\n\
                This event promises to be impactful as it explores the intersection of Blockchain and the Fourth Industrial Revolution. \
                Blockchain technology is more than just another tech innovation; it lies at the core of the Fourth Industrial Revolution (4IR). \
                It possesses the transformative power to reshape industries such as finance, healthcare, and logistics. \n\n\
                Come gain an international perspective that transcends national borders. We have extended invitations to speakers and guests from \
                various countries, including Kenya and Switzerland. \n\n\
                Kindly note that your application has been received and is slated for review by our development team within 24 hours. \
                While you wait, kindly connect with us via our website; you can also access our open-source repository \
                (<a href="http://github.com/ujblockchain" target="_blank" style="color: #ff6522 !important;">github.com/ujblockchain</a>) \
                for code guides and tips.\n\n\
                Once again, thank you for applying for the Mainstreaming Blockchain Event. We are excited and cannot wait to see the many frontiers \
                this will open for you in your Blockchain Development Journey 🤩🙌.\
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
            program_flyer = f'{settings.PROJECT_DIR}/static/images/flyer.jpg'
            msg.attach_file(program_flyer)

            # send email
            msg.send()
        else:
            # once model is saved, trigger signal
            if instance.application_status == 'Selected':
                email_subject = 'You Have Been Selected 🥳🎉: Mainstreaming Blockchain (MB)'
                email_message = f'Hi {instance.first_name},\n\n\
                    Thank you for your interest and selection to attend the Mainstreaming Blockchain (MB): \
                    A Thought Leadership Media Event. Mainstreaming Blockchain is set to take place on October 24, 2023. Organized by \
                    the SA/Swiss Chair on Blockchain Technology at the University of Johannesburg, this event will bring together blockchain \
                    enthusiasts, industry experts, researchers, and thought leaders. Its primary focus is to delve into the immense potential \
                    of blockchain technology in South and Sub-Saharan Africa. \n\n\
                    This event promises to be impactful as it explores the intersection of Blockchain and the Fourth Industrial Revolution. \
                    Blockchain technology is more than just another tech innovation; it lies at the core of the Fourth Industrial Revolution (4IR). \
                    It possesses the transformative power to reshape industries such as finance, healthcare, and logistics. \n\n\
                    Come gain an international perspective that transcends national borders. We have extended invitations to speakers and guests from \
                    various countries, including Kenya and Switzerland. \n\n\
                    Kindly note that you have been selected to attend the Mainstreaming Blockchain (MB) event. The event takes place at \
                    <strong>STH Auckland Park Bunting Road Campus. Time is 8:30am </strong>. While you wait, kindly connect with us via our website; \
                    you can also access our open-source repository (<a href="http://github.com/ujblockchain" target="_blank" style="color: #ff6522 !important;">github.com/ujblockchain</a>) \
                    for code guides and tips.\n\n\
                    Once again, thank you for applying for the Mainstreaming Blockchain (MB) Event. We are excited and cannot wait to see the many frontiers \
                    this will open for you in your Blockchain Development Journey 🤩🙌.\
                '

                email_link = 'https://blockchain.uj.ac.za'
                email_link_title = 'UJ Blockchain'

            elif instance.application_status == 'Rejected':
                email_subject = 'Application Status: Mainstreaming Blockchain (MB)'
                email_message = f'Hi {instance.first_name},\n\n\
                    Thank you for your interest and selection to attend the Mainstreaming Blockchain (MB): \
                    A Thought Leadership Media Event. Mainstreaming Blockchain is set to take place on October 24, 2023. Organized by \
                    the SA/Swiss Chair on Blockchain Technology at the University of Johannesburg, this event will bring together blockchain \
                    enthusiasts, industry experts, researchers, and thought leaders. Its primary focus is to delve into the immense potential \
                    of blockchain technology in South and Sub-Saharan Africa. \n\n\
                    Unfortunately, you were not selected for the Mainstreaming Blockchain (MB) event. We received large volumes of applications for \
                    the event, but we could only take a few. \n\n\
                    We understand your desire to attend this event and your drive to gain a better perspective in Blockchain; yes, we do. There will be \
                    other Events coming up; to ensure you register in time, sign up for our newsletter. Our newsletters gives you up-to-date \
                    insight into our build stacks and projects we are currently working on. It also gives you the privilege of getting early \
                    registration links for Bootcamps, Hackathon, and other programs like this three days before it is made open to the general public.\n\n\
                    Once again, thank you for applying for the Mainstreaming Blockchain (MB) Event. We are excited and cannot wait to see the many frontiers \
                    upcoming events will open for you in your Blockchain Development Journey 🤩🙌.\
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
                program_flyer = f'{settings.PROJECT_DIR}/static/images/flyer.jpg'
                msg.attach_file(program_flyer)

            # send email
            msg.send()
