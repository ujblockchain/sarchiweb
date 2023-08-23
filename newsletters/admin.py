from django.contrib import admin
from .models import NewsletterEmail


class NewsletterAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'timestamp',
    ]
    list_display_links = [
        'email',
        'timestamp',
    ]
    search_fields = [
        'email',
        'timestamp',
    ]
    readonly_fields = [
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
    fields = ['email', 'timestamp']


#
admin.site.register(NewsletterEmail, NewsletterAdmin)
