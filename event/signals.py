from random import randint
from django.conf import settings
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string


from project.settings import env
from .models import EventRegistration


@receiver(post_save, sender=EventRegistration)
def auto_mail_sending(sender, instance, created, **kwargs):

    recipient_email = [instance.email]
    sender_email = settings.DEFAULT_FROM_EMAIL
    email_subject = None
    html_content = None

    if created:
        email_subject = "Application Received - UJ Blockchain x H.E.R DAO"

        html_content = render_to_string(
            'emails/event_apply.html',
            {
                'first_name': instance.first_name,
            },
        )

    else:
        if instance.status == 'selected':
            email_subject = "You're Accepted! - UJ Blockchain x H.E.R DAO"
            message_text = (
                "We are absolutely thrilled to inform you that you have been selected to participate in "
                "the <strong>UJ Blockchain x H.E.R DAO Training Program</strong>! and "
                "we are excited to help you dive deeper into Web3.\n\n"
                "Venue: <strong>Department of Electrical and Electronic Engineering Science, "
                "Lab B2 219, University of Johannesburg, Auckland Park Campus</strong>."
            )

            html_content = render_to_string(
                'emails/event_selected.html',
                {
                    'first_name': instance.first_name,
                    'email_message': message_text,
                    'group_link': 'https://www.linkedin.com/company/south-africa-swiss-bilateral-research-chair-in-blockchain-technology/',
                },
            )
        elif instance.status == 'rejected':
            email_subject = "Application Update - UJ Blockchain x H.E.R DAO"

            html_content = render_to_string(
                'emails/event_rejected.html',
                {
                    'first_name': instance.first_name,
                },
            )

    if not html_content or not email_subject:
        return

    msg = mail.EmailMessage(
        email_subject,
        html_content,
        sender_email,
        recipient_email,
        reply_to=[env.get('ADMIN_REPLY_EMAIL')],
        headers={
            'X-PM-Message-Stream': 'outbound',
            'Message-ID': f'<{randint(1, 1000)}@ujblockchain.co.za>',
        },
    )

    msg.content_subtype = 'html'
    if created or instance.status == 'selected':
        event_flyer = f'{settings.PROJECT_DIR}/static/img/event.jpeg'
        msg.attach_file(event_flyer)

    msg.send(fail_silently=True)
