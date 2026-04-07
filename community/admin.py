from django.contrib import admin
from .models import CommunityRegistration
from import_export.admin import ImportExportActionModelAdmin


@admin.register(CommunityRegistration)
class CummunityApplicationAdmin(ImportExportActionModelAdmin):
    list_display = ['first_name', 'last_name', 'faculty', 'department', 'created_at']
    list_display_links = ['first_name', 'last_name', 'faculty', 'department']
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions_on_top = True
    readonly_fields = ['id', 'created_at']
    save_as = True
    save_as_continue = True
    show_full_result_count = True
    save_on_top = True
    search_fields = ['first_name', 'last_name', 'faculty', 'department']
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'faculty',
        'department',
        'nationality',
        'year_of_study',
        'created_at',
    ]
