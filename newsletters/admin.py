from django.contrib import admin
from .models import NewsletterEmail


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


#
admin.site.register(NewsletterEmail, NewsletterAdmin)
