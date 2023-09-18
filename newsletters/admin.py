from django.contrib import admin
from .models import NewsletterEmail, SendNewsletterEmails


class NewsletterAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'timestamp',
    ]
    list_display_links = [
        'id',
        'email',
        'timestamp',
    ]
    search_fields = [
        'id',
        'email',
        'timestamp',
    ]
    readonly_fields = [
        'id',
        'email',
        'timestamp',
    ]
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fields = ['id', 'email', 'timestamp']


class SendNewsletterEmailsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'subject',
        'group',
        'timestamp',
    ]
    list_display_links = [
        'id',
        'subject',
        'group',
        'timestamp',
    ]
    list_filter = ['group']
    search_fields = [
        'id',
        'subject',
        'group',
        'link',
        'link_title',
        'timestamp',
    ]
    readonly_fields = [
        'id',
    ]
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fieldsets = [
        [
            'General Information',
            {
                'classes': ['wide'],
                'fields': [
                    'id',
                    'subject',
                    'group',
                ],
            },
        ],
        [
            'Message Details',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'message',
                    'salutation',
                ],
            },
        ],
        [
            'Link Details',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['link', 'link_title'],
            },
        ],
        [
            'Last Updated',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'timestamp',
                ],
            },
        ],
    ]


# register models
admin.site.register(NewsletterEmail, NewsletterAdmin)
admin.site.register(SendNewsletterEmails, SendNewsletterEmailsAdmin)
