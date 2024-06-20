from django.apps import AppConfig


class MasterclassConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'masterclass'

    def ready(self):
        import masterclass.signals