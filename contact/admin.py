from django.contrib import admin
from .models import UserContact


class UserContactAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'phone',
        'message',
        'timestamp',
    ]
    list_display_links = [
        'name',
        'email',
        'phone',
        'message',
    ]
    search_fields = [
        'name',
        'email',
        'phone',
        'message',
        'timestamp',
    ]
    readonly_fields = [
        'name',
        'email',
        'phone',
        'message',
        'timestamp',
    ]
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fields = ['name', 'email', 'phone', 'message', 'timestamp']


#
admin.site.register(UserContact, UserContactAdmin)