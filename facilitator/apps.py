from django.apps import AppConfig


class FacilitatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facilitator'
    icon = 'fas fa-users-cog'
    hide = False

    def ready(self):
        import facilitator.signals
