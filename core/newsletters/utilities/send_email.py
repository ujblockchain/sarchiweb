from random import randint

from decouple import config
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string


# handles email sending
def send_email(salutation, subject, message, link, link_title, email_list):
    # init email details
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_email = email_list
    email_salutation = salutation
    email_subject = subject
    email_message = message
    email_link = link
    email_link_title = link_title

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
        subject=email_subject,
        body=html_content,
        from_email=sender_email,
        bcc=recipient_email,
        reply_to=[config('ADMIN_REPLY_EMAIL')],
        headers={
            'X-PM-Message-Stream': 'outbound',
            'Message-ID': f'{randint(1, 1000)}',
        },
    )

    # ensure that email format is html
    msg.content_subtype = 'html'

    # attached bootcamp flier
    bootcamp_flyer = f'{settings.PROJECT_DIR}/static/images/Bootcamp.png'
    msg.attach_file(bootcamp_flyer)

    # send email
    msg.send()


# handles email sending
def send_bootcamp_reminder_email(
    subject, main_message_heading, primary_message_section, image_session_heading, display_image_1,
    display_image_1_text, display_image_2, display_image_2_text, display_image_3, display_image_3_text,
    display_image_4, display_image_4_text, secondary_message_section, email_list
):
    # init email details
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_email = email_list
    email_subject = subject

    # use email template
    html_content = render_to_string(
        'email/bootcamp.html',
        {  # pass context to email template
            'main_message_heading': main_message_heading,
            'primary_message_section': primary_message_section,
            'image_session_heading': image_session_heading,
            'display_image_1': display_image_1,
            'display_image_1_text': display_image_1_text,
            'display_image_2': display_image_2,
            'display_image_2_text': display_image_2_text,
            'display_image_3': display_image_3,
            'display_image_3_text': display_image_3_text,
            'display_image_4': display_image_4,
            'display_image_4_text': display_image_4_text,
            'secondary_message_section': secondary_message_section
        },
    )

    # create HTML email.
    msg = mail.EmailMessage(
        subject=email_subject,
        body=html_content,
        from_email=sender_email,
        bcc=recipient_email,
        reply_to=[config('ADMIN_REPLY_EMAIL')],
        headers={
            'X-PM-Message-Stream': 'outbound',
            'Message-ID': f'{randint(1, 1000)}',
        },
    )

    # ensure that email format is html
    msg.content_subtype = 'html'

    # attached bootcamp flier
    bootcamp_flyer = f'{settings.PROJECT_DIR}/static/images/Bootcamp.png'
    msg.attach_file(bootcamp_flyer)

    # send email
    msg.send()
