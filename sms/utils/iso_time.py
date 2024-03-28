from pytz import timezone, utc
from django.conf import settings

# get project timezone
tz = timezone(settings.TIME_ZONE)


def isoformat(dt):

    # return object in ISO 8601 format adding without microseconds or time offset
    return tz.localize(dt.replace(microsecond=0)).astimezone(utc).replace(tzinfo=None).isoformat() + 'Z'
