from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'
    icon = 'fas fa-user-friends'
    hide = False
    divider_title = 'Apps'

    def ready(self):
        import community.signals
