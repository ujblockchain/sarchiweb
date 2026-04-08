from django.contrib import admin
from import_export import resources
from .models import EventRegistration
from import_export.admin import ImportExportActionModelAdmin


class EventResource(resources.ModelResource):
    class Meta:
        model = EventRegistration
        chunk_size = 2000

    def get_queryset(self):
        return super().get_queryset().select_related()

    def filter_export(self, queryset, **kwargs):
        return queryset


@admin.register(EventRegistration)
class EventApplicationAdmin(ImportExportActionModelAdmin):
    resource_classes = [EventResource]
    list_display = ['first_name', 'last_name', 'faculty', 'department', 'created_at', 'status']
    list_display_links = ['first_name', 'last_name', 'faculty', 'department']
    list_filter = ['status']
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions_on_top = True
    readonly_fields = ['id', 'created_at']
    save_as = True
    save_as_continue = True
    search_fields = ['first_name', 'last_name', 'faculty', 'department', 'status']
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'faculty',
        'department',
        'nationality',
        'year_of_study',
        'status',
        'created_at',
    ]
