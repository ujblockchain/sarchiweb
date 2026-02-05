import ast

from django.utils import timezone

# init current time
current_timestamp = timezone.now()


def dateformat(value):
    return f'{value.strftime("%B")} {value.strftime("%d")}, {value.strftime("%Y")}'


# convert dict to string
def dict_string(value):
    return ast.literal_eval(value)


def event_dateformat(value):
    return f'{value.strftime("%d")}/{value.strftime("%m")}'
