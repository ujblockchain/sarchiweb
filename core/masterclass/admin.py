from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reversion_compare.admin import CompareVersionAdmin

from .models import Masterclass, MasterclassConfig


class MasterclassResource(resources.ModelResource):

    class Meta:
        model = Masterclass
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = (
            'first_name', 'last_name', 'can_you_code', 'gender', 'email', 'faculty', 'department', 'level',
            'student_number', 'nationality', 'phone_number', 'expectation', 'application_status'
        )
        export_id_fields = (
            'first_name', 'last_name', 'gender', 'email', 'faculty', 'department', 'level', 'student_number',
            'nationality', 'phone_number', 'repo_link', 'application_status', 'date_created'
        )


class MasterclassConfigAdmin(admin.ModelAdmin):
    list_display = ['masterclass_title', 'opening_date', 'closing_date', 'last_update']
    list_display_links = ['masterclass_title', 'opening_date', 'closing_date', 'last_update']
    search_fields = ['masterclass_title', 'opening_date', 'closing_date', 'last_update']
    readonly_fields = ['last_update', 'info']
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True

    field = ['masterclass_title', 'opening_date', 'closing_date', 'last_update', 'info']

    # add custom field
    @admin.display(description='Notice')
    def info(self, obj):
        return format_html(
            "<span style='color: #454d55; padding: 10px; font-size: 13px; font-style: italic; background: #ef9a9a; border-radius: 50px;'>Masterclass registration auto disable after closing date</span>"  # noqa: E501
        )


class MasterclassAdmin(ImportExportModelAdmin, CompareVersionAdmin):
    resource_class = MasterclassResource
    list_display = [
        'first_name', 'last_name', 'gender', 'email', 'phone_number', 'faculty', 'department', 'level',
        'student_number', 'nationality', 'application_status', 'timestamp'
    ]
    list_display_links = [
        'first_name', 'last_name', 'faculty', 'department', 'level', 'student_number', 'application_status'
    ]
    list_filter = ['application_status']
    search_fields = [
        'first_name', 'last_name', 'gender', 'email', 'faculty', 'department', 'level', 'student_number',
        'nationality', 'expectation', 'phone_number', 'application_status', 'timestamp'
    ]
    readonly_fields = [
        'info',
    ]
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
                'fields': ['first_name', 'last_name', 'gender', 'email', 'nationality', 'phone_number', 'info'],
            },
        ],
        [
            'Department Summary',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['faculty', 'department', 'level', 'student_number'],
            },
        ],
        [
            'User Sessions',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['repo_link'],
            },
        ],
        [
            'Application Details',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['expectation'],
            },
        ],
        [
            'Application Status',
            {
                'classes': ['collapse'],
                'fields': ['application_status'],
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

    # add custom field
    @admin.display(description='Notice')
    def info(self, obj):
        return format_html(
            "<span style='color: #454d55; padding: 10px; font-size: 13px; font-style: italic; background: #ef9a9a; border-radius: 50px;'>All mails are handled automatically and delivered using signup email</span>"  # noqa: E501
        )


# register admin settings
admin.site.register(MasterclassConfig, MasterclassConfigAdmin)
admin.site.register(Masterclass, MasterclassAdmin)
