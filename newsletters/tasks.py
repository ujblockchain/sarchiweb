from django_huey import task, on_startup, signal
from huey_monitor.tasks import startup_handler, store_signals
from .utilities.send_email import send_email

# huey monitor setup for send emails queue.
# this will enable us to track task in the admin
signal(queue='send_emails')(store_signals)
on_startup(queue='send_emails')(startup_handler)


# set as a periodic task to run every one minute
@task(queue='send_emails')
def send_email_task(email_list, salutation, subject, message, link, link_title):
    # send email
    # loop email list
    for i in email_list:
        send_email(salutation, subject, message, link, link_title, i)
