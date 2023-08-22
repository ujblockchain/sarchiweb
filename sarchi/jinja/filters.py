import ast
from datetime import datetime
from django.utils.timezone import utc


# init current time
current_timestamp = datetime.now().replace(tzinfo=utc)


def dateformat(value):
    return f'{value.strftime("%B")} {value.strftime("%d")}, {value.strftime("%Y")}'


# convert dict to string
def dict_string(value):
    return ast.literal_eval(value)


# get hour different from current time
def time_since(value):
    difference = current_timestamp - value

    # init days and seconds
    days = difference.days
    seconds = difference.seconds

    # init hours
    hours = days * 24 + seconds // 3600

    return hours
