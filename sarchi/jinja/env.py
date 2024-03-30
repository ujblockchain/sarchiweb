from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
from jinja2 import Environment
from .filters import dateformat, dict_string, static_integrity


def JinjaEnvironment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse,
        'trim_blocks': True,
        'Istrip_blocks': True,
        'static': staticfiles_storage.url,
    })
    env.filters.update({
        'dateformat': dateformat,
        'dictstring': dict_string,
        'static_integrity': static_integrity,
    })

    return env
