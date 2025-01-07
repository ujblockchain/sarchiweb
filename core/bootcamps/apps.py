from django.apps import AppConfig


class BootcampsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.bootcamps'

    def ready(self):
        import core.bootcamps.signals
