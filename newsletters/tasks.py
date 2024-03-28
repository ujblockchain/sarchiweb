from django_huey import task, on_startup, signal
from huey_monitor.tasks import startup_handler, store_signals
from .utilities.send_email import send_bootcamp_reminder_email, send_email

# huey monitor setup for send emails queue.
# this will enable us to track task in the admin
signal(queue='send_emails')(store_signals)
on_startup(queue='send_emails')(startup_handler)
#
signal(queue='bootcamp_reminder_emails')(store_signals)
on_startup(queue='bootcamp_reminder_emails')(startup_handler)


# set task
@task(queue='send_emails')
def send_email_task(email_list, salutation, subject, message, link, link_title):
    # send email
    # loop email list
    for i in email_list:
        send_email(salutation, subject, message, link, link_title, i)


# set task
@task(queue='bootcamp_reminder_emails')
def reminder_email_task(email_list, subject, main_message_heading, primary_message_section, image_section_heading,
                        display_image_1, display_image_1_text, display_image_2, display_image_2_text, display_image_3,
                        display_image_3_text, display_image_4, display_image_4_text, secondary_message_section):
    # send email
    # loop email list
    for i in email_list:
        send_bootcamp_reminder_email(subject, main_message_heading, primary_message_section, image_section_heading,
                                     display_image_1, display_image_1_text, display_image_2, display_image_2_text,
                                     display_image_3, display_image_3_text, display_image_4, display_image_4_text,
                                     secondary_message_section, i)