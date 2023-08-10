from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
from jinja2 import Environment
from .filters import dateformat


def JinjaEnvironment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            'static': staticfiles_storage.url,
            'url': reverse,
            'trim_blocks': True,
            'Istrip_blocks': True,
        }
    )
    env.filters.update(
        {
            'dateformat': dateformat,
        }
    )

    return env
