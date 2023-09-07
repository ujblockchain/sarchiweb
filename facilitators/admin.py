from django.contrib import admin
from .models import Facilitators


class FacilitatorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'role',
        'phone_number',
        'image',
        'publish',
        'timestamp',
    ]
    list_display_links = [
        'id',
        'full_name',
        'role',
        'phone_number',
        'image',
    ]
    search_fields = [
        'id',
        'full_name',
        'role',
        'phone_number',
        'image',
        'publish',
        'timestamp',
    ]
    readonly_fields = ['id']
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fields = ['id', 'full_name', 'role', 'phone_number', 'image', 'publish', 'timestamp']


#
admin.site.register(Facilitators, FacilitatorAdmin)
