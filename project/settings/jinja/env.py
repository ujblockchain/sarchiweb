from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def JinjaEnvironment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            'url': reverse,
            'trim_blocks': True,
            'Istrip_blocks': True,
            'static': static,
        }
    )
    # env.filters.update({})

    return env
