from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reversion_compare.admin import CompareVersionAdmin

from core.blog.admin import visibility_action

from .models import ProgramConfig, ProgramSignUp, ProjectBuild


class ProgramResource(resources.ModelResource):

    class Meta:
        model = ProgramSignUp
        skip_unchanged = True
        report_skipped = True
        exclude = ['id']
        import_id_fields = ['email']


class ProgramConfigAdmin(admin.ModelAdmin):
    list_display = ['event_title', 'opening_date', 'closing_date', 'last_update']
    list_display_links = ['event_title', 'opening_date', 'closing_date', 'last_update']
    search_fields = ['event_title', 'opening_date', 'closing_date', 'last_update']
    readonly_fields = ['last_update', 'info']
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True

    field = ['event_title', 'opening_date', 'closing_date', 'last_update', 'info']

    # add custom field
    @admin.display(description='Notice')
    def info(self, obj):
        return format_html(
            "<span style='color: #454d55; padding: 10px; font-size: 13px; font-style: italic; \
            background: #ef9a9a; border-radius: 50px;'>Program registration auto \
            disable after closing date</span>"
        )


class ProgramSignupAdmin(ImportExportModelAdmin, CompareVersionAdmin):
    resource_class = ProgramResource
    list_display = [
        'first_name', 'last_name', 'gender', 'email', 'phone_number', 'nationality', 'organization',
        'application_status', 'timestamp'
    ]
    list_display_links = ['first_name', 'last_name', 'email', 'organization', 'application_status']
    list_filter = ['application_status']
    search_fields = [
        'first_name', 'last_name', 'gender', 'email', 'nationality', 'expectation', 'phone_number', 'organization',
        'application_status', 'timestamp'
    ]
    readonly_fields = [
        'info',
    ]
    date_hierarchy = 'timestamp'
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
                'fields': [
                    'first_name', 'last_name', 'gender', 'email', 'nationality', 'phone_number', 'organization', 'info'
                ],
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
            "<span style='color:#ef9a9a; ;'>All mails are handled automatically and delivered using signup email"
        )


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_id', 'title', 'project_progress', 'project_commit_count', 'distribution_count',
        'total_distribution_count', 'lines_of_code', 'coding_hours', 'project_start_time', 'project_end_time',
        'last_update'
    ]
    list_display_links = [
        'project_id', 'title', 'project_progress', 'project_commit_count', 'distribution_count',
        'total_distribution_count', 'lines_of_code', 'coding_hours', 'project_start_time', 'project_end_time'
    ]
    list_filter = ['publish']
    search_fields = [
        'project_id', 'title', 'project_progress', 'project_commit_count', 'distribution_count',
        'total_distribution_count', 'lines_of_code', 'coding_hours', 'project_start_time', 'project_end_time',
        'last_update'
    ]
    readonly_fields = ['project_id', 'slug']
    list_per_page = 50
    show_full_result_count = True
    actions = [visibility_action]
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
                'fields': ['project_id', 'title', 'project_progress', 'project_start_time', 'project_end_time'],
            },
        ],
        [
            'Project Summary',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'summary', 'project_commit_count', 'distribution_count', 'total_distribution_count',
                    'lines_of_code', 'coding_hours'
                ],
            },
        ],
        [
            'Project Stages',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'distribution_section_stats', 'distribution_section_stats_end',
                    'distribution_section_stats_end_summary', 'current_stage_section_end_time'
                ],
            },
        ],
        [
            'Visibility and Control',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['publish', 'schedule_message'],
            },
        ],
        [
            'Last Updated',
            {
                'classes': ['collapse', 'wide'],
                'fields': ['last_update'],
            },
        ],
    ]


# register model
admin.site.register(ProgramConfig, ProgramConfigAdmin)
admin.site.register(ProjectBuild, ProjectAdmin)
admin.site.register(ProgramSignUp, ProgramSignupAdmin)
