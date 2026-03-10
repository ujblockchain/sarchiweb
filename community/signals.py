from random import randint
from django.conf import settings
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string


from project.settings import env
from .models import CommunityRegistration


@receiver(post_save, sender=CommunityRegistration)
def auto_mail_sending(sender, instance, created, **kwargs):

    if created:
        recipient_email = [instance.email]
        sender_email = settings.DEFAULT_FROM_EMAIL
        email_subject = "Welcome to the Community - UJ Blockchain"

        html_content = render_to_string(
            'emails/community.html',
            {
                'first_name': instance.first_name,
            },
        )
        

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
        msg.send(fail_silently=True)
