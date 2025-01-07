from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'last_update']
    list_display_links = ['title', 'date', 'last_update']
    search_fields = ['title', 'event_info', 'date', 'last_update']
    readonly_fields = ['last_update']
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as_continue = True
    save_on_top = True

    field = ['title', 'event_info', 'date', 'link_type', 'registration_link', 'event_website', 'image', 'last_update']


# register admin settings
admin.site.register(Event, EventAdmin)
