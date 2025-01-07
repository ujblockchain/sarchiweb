from huey.contrib.djhuey import task

from .utilities.send_email import send_bootcamp_reminder_email, send_email


# set task
@task()
def send_email_task(email_list, salutation, subject, message, link, link_title):
    # send email
    # loop email list
    for i in email_list:
        send_email(salutation, subject, message, link, link_title, i)


# set task
@task()
def reminder_email_task(
    email_list, subject, main_message_heading, primary_message_section, image_section_heading, display_image_1,
    display_image_1_text, display_image_2, display_image_2_text, display_image_3, display_image_3_text,
    display_image_4, display_image_4_text, secondary_message_section
):
    # send email
    # loop email list
    for i in email_list:
        send_bootcamp_reminder_email(
            subject, main_message_heading, primary_message_section, image_section_heading, display_image_1,
            display_image_1_text, display_image_2, display_image_2_text, display_image_3, display_image_3_text,
            display_image_4, display_image_4_text, secondary_message_section, i
        )
