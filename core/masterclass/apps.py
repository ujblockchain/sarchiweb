from django.apps import AppConfig


class MasterclassConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.masterclass'

    # def ready(self):
    #     import core.masterclass.signals