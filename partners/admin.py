from django.contrib import admin
from .models import Partners


class PartnersAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image',
        'publish',
        'timestamp',
    ]
    list_display_links = [
        'name',
        'image',
    ]
    search_fields = [
        'name',
        'image',
        'publish',
        'timestamp',
    ]
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fields = ['name', 'image', 'publish', 'timestamp']


#
admin.site.register(Partners, PartnersAdmin)
