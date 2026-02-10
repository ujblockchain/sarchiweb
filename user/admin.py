from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Users


class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	change_password_form = AdminPasswordChangeForm

	list_display = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
	list_display_links = ['first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
	list_filter = ['is_active', 'is_staff', 'is_superuser']
	date_hierarchy = 'date_joined'
	readonly_fields = ['id', 'date_joined', 'last_login']
	search_fields = ['first_name', 'last_name', 'email']
	list_per_page = 100
	ordering = ['-date_joined']

	fieldsets = [
		[
			None,
			{'fields': ['email', 'password']},
		],
		[
			'Personal info',
			{'fields': ['first_name', 'last_name']},
		],
		[
			'Permissions',
			{'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']},
		],
		[
			'Important dates',
			{'fields': ['last_login', 'date_joined']},
		],
	]

	add_fieldsets = [
		[
			None,
			{
				'classes': ['wide'],
				'fields': ['first_name', 'last_name', 'email', 'password1', 'password2'],
			},
		],
	]


# register custom user
admin.site.register(Users, CustomUserAdmin)
