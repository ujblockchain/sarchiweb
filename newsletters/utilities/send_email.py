from random import randint
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from decouple import config
from sarchi.middleware.current_request import RequestMiddleware

#handles email sending
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
