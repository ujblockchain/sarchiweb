from django.apps import AppConfig


class EventConfig(AppConfig):
    name = 'event'
    icon = 'fas fa-calendar'
    hide = False

    # def ready(self):
    #     import event.signals
