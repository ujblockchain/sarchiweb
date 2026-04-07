from django.contrib import admin
from import_export import resources
from .models import StudentApplication
from import_export.admin import ImportExportActionModelAdmin


class StudentResource(resources.ModelResource):
    class Meta:
        model = StudentApplication
        chunk_size = 2000

    def get_queryset(self):
        return super().get_queryset().select_related()

    def filter_export(self, queryset, **kwargs):
        return queryset


@admin.register(StudentApplication)
class StudentApplicationAdmin(ImportExportActionModelAdmin):
    resource_classes = [StudentResource]
    list_display = ['first_name', 'last_name', 'faculty', 'department', 'created_at']
    list_display_links = ['first_name', 'last_name', 'faculty', 'department']
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions_on_top = True
    readonly_fields = ['id', 'created_at']
    save_as = True
    save_as_continue = True
    search_fields = ['first_name', 'last_name', 'faculty', 'department']
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'faculty',
        'department',
        'nationality',
        'year_of_study',
        'ieee_membership',
        'saiee_membership',
        'other_membership',
        'created_at',
    ]
