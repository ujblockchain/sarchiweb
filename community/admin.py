from django.contrib import admin
from import_export import resources
from .models import CommunityRegistration
from import_export.admin import ImportExportActionModelAdmin


class CommunityResource(resources.ModelResource):
    class Meta:
        model = CommunityRegistration
        chunk_size = 2000

    def get_queryset(self):
        return super().get_queryset().select_related()

    def filter_export(self, queryset, **kwargs):
        return queryset


@admin.register(CommunityRegistration)
class CummunityApplicationAdmin(ImportExportActionModelAdmin):
    resource_classes = [CommunityResource]
    list_display = ['first_name', 'last_name', 'faculty', 'department', 'created_at']
    list_display_links = ['first_name', 'last_name', 'faculty', 'department']
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions_on_top = True
    readonly_fields = ['id', 'created_at']
    save_as = True
    save_as_continue = True
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
