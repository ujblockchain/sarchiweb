from django.apps import AppConfig


class ProgramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.program'

    # def ready(self):
    #     import core.program.signals
