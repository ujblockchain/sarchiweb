from django.contrib import admin
from .models import SendUserSms


class SendUserSmsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'group', 'timestamp']
    list_display_links = ['id', 'title', 'group', 'timestamp']
    list_filter = ['group']
    search_fields = ['id', 'title', 'group', 'timestamp']
    readonly_fields = ['id', 'timestamp']
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as_continue = True
    save_on_top = True
    fieldsets = [
        [
            'General Information',
            {
                'classes': ['wide'],
                'fields': ['id', 'title', 'group'],
            },
        ],
        [
            'Message Details',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['message'],
            },
        ],
        [
            'Creation Date/Time',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['timestamp'],
            },
        ],
    ]


# register models
admin.site.register(SendUserSms, SendUserSmsAdmin)
