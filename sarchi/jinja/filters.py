import ast
from datetime import datetime
from django.utils.timezone import utc
from sri.templatetags.sri import sri_integrity_static

# init current time
current_timestamp = datetime.now().replace(tzinfo=utc)


def dateformat(value):
    return f'{value.strftime("%B")} {value.strftime("%d")}, {value.strftime("%Y")}'


# convert dict to string
def dict_string(value):
    return ast.literal_eval(value)


# hack to work with sri: temp
def static_integrity(value):
    return sri_integrity_static(path=value)
