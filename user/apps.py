from django.apps import AppConfig


class UserConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'user'
	icon = 'fas fa-user-shield'
	divider_title = 'Auth'
	priority = 1
	hide = False
