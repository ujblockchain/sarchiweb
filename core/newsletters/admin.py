from django.contrib import admin

from .models import NewsletterEmail, SendBootcampReminderEmails, SendUserEmails


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'timestamp']
    list_gallery_links = ['id', 'email', 'timestamp']
    search_fields = ['id', 'email', 'timestamp']
    readonly_fields = ['id', 'email', 'timestamp']
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fields = ['id', 'email', 'timestamp']


class SendUserEmailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'group', 'timestamp']
    list_gallery_links = ['id', 'subject', 'group', 'timestamp']
    list_filter = ['group']
    search_fields = ['id', 'subject', 'group', 'link', 'link_title', 'timestamp']
    readonly_fields = ['id']
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
                'fields': ['id', 'subject', 'group'],
            },
        ],
        [
            'Message Details',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['message', 'salutation'],
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
                'fields': ['timestamp'],
            },
        ],
    ]


class ReminderEmailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'group', 'timestamp']
    list_gallery_links = ['id', 'subject', 'group', 'timestamp']
    list_filter = ['group']
    search_fields = [
        'id', 'subject', 'group', 'main_message_heading', 'timestamp', 'primary_message_section',
        'gallery_image_1_text', 'gallery_image_2_text', 'gallery_image_3_text', 'gallery_image_4_text',
        'secondary_message_section'
    ]
    readonly_fields = ['id', 'timestamp']
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
                'fields': ['id', 'subject', 'group'],
            },
        ],
        [
            'Message Details',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['main_message_heading', 'primary_message_section', 'secondary_message_section'],
            },
        ],
        [
            'Image Details',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'image_section_heading', 'gallery_image_1', 'gallery_image_1_text', 'gallery_image_2',
                    'gallery_image_2_text', 'gallery_image_3', 'gallery_image_3_text', 'gallery_image_4',
                    'gallery_image_4_text'
                ],
            },
        ],
        [
            'Last Updated',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['timestamp'],
            },
        ],
    ]


# register models
admin.site.register(NewsletterEmail, NewsletterAdmin)
admin.site.register(SendUserEmails, SendUserEmailsAdmin)
admin.site.register(SendBootcampReminderEmails, ReminderEmailsAdmin)
