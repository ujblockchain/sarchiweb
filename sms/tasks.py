from django_huey import task, on_startup, signal
from huey_monitor.tasks import startup_handler, store_signals
from .utils.send_sms import send_sms

# huey monitor setup for send emails queue.
# this will enable us to track task in the admin
signal(queue='send_sms')(store_signals)
on_startup(queue='send_sms')(startup_handler)


# set task
@task(queue='send_sms')
def send_sms_task(sms_list, message, delivery_time):
    # send sms
    # loop number list
    for i in sms_list:
        send_sms(i, message, delivery_time)
