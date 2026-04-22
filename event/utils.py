from django.conf import settings
from django.core.mail import EmailMessage, make_msgid
from django.template.loader import render_to_string
from django.template import Template, Context
from .models import EventEmailConfig
from project.settings import env


def get_db_email_config(model_class):
    model_name = model_class._meta.model_name
    search_term = None

    if model_name == 'eventregistration':
        search_term = 'ujb'
    elif model_name == 'fewsregistration':
        search_term = 'fews'
    else:
        search_term = model_name
    return EventEmailConfig.objects.filter(event_type__icontains=search_term).first()


def send_single_status_email(instance, status):
    config = get_db_email_config(instance.__class__)
    if not config:
        return

    # grab all fields dynamically
    context_data = {
        field.name: getattr(instance, field.name) for field in instance._meta.fields
    }

    # dynamically get the right subject and text fields
    subject_text = getattr(config, f"{status}_subject")
    message_content = getattr(config, f"{status}_message_text")

    # render template
    db_template = Template(message_content)
    formatted_message = db_template.render(Context(context_data))

    html_content = render_to_string(
        f'emails/{config.event_type.lower()}_{status}_event.html',
        {
            'email_message': formatted_message,
            'group_link': config.group_link,
        },
    )

    msg = EmailMessage(
        subject=subject_text,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[instance.email],
        reply_to=[env.get('ADMIN_REPLY_EMAIL', settings.DEFAULT_FROM_EMAIL)],
        headers={'Message-ID': make_msgid(domain='ujblockchain.co.za')},
    )
    msg.content_subtype = 'html'

    if config.attachment and config.attachment.name:
        msg.attach_file(config.attachment.path)

    msg.send(fail_silently=False)


def send_bulk_status_email(model_class, bcc_emails, status):
    config = get_db_email_config(model_class)
    if not config:
        return

    # dynamically get the bulk text and subject
    subject_text = getattr(config, f"{status}_subject")
    bulk_message_content = getattr(config, f"{status}_bulk_message_text")

    db_template = Template(bulk_message_content)
    formatted_message = db_template.render(Context({}))

    html_content = render_to_string(
        f'emails/{config.event_type.lower()}_{status}_event.html',
        {
            'email_message': formatted_message,
            'group_link': config.group_link,
        },
    )

    msg = EmailMessage(
        subject=subject_text,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL],
        bcc=bcc_emails,
        reply_to=[env.get('ADMIN_REPLY_EMAIL', settings.DEFAULT_FROM_EMAIL)],
        headers={'Message-ID': make_msgid(domain='ujblockchain.co.za')},
    )
    msg.content_subtype = 'html'

    if config.attachment and config.attachment.name:
        msg.attach_file(config.attachment.path)

    msg.send(fail_silently=False)
