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
