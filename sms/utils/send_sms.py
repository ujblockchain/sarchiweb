from decouple import config
from twilio.rest import Client

# init sms client
client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))


# handles sms sending
def send_sms(phone_number, message):
    # send message
    client.messages.create(
        body=message,
        from_=config('TWILIO_PHONE_NUMBER'),
        to=phone_number,
    )
