from huey.contrib.djhuey import task

from .utils.send_sms import send_sms


# set task
@task()
def send_sms_task(sms_list, message):
    # send sms
    # loop number list
    for i in sms_list:
        send_sms(i, message)
