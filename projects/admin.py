from django.contrib import admin
from blog.admin import visibility_action
from .models import Projects


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'project_progress',
        'project_commit_count',
        'distribution_count',
        'total_distribution_count',
        'lines_of_code',
        'coding_hours',
        'project_start_time',
        'project_end_time',
        'last_update',
    ]
    list_display_links = [
        'id',
        'title',
        'project_progress',
        'project_commit_count',
        'distribution_count',
        'total_distribution_count',
        'lines_of_code',
        'coding_hours',
        'project_start_time',
        'project_end_time',
    ]
    list_filter = [
        'publish',
    ]
    search_fields = [
        'id',
        'title',
        'project_progress',
        'project_commit_count',
        'distribution_count',
        'total_distribution_count',
        'lines_of_code',
        'coding_hours',
        'project_start_time',
        'project_end_time',
        'last_update',
    ]
    readonly_fields = ['id', 'slug']
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
                'fields': [
                    'id',
                    'title',
                    'project_progress',
                    'project_start_time',
                    'project_end_time',
                ],
            },
        ],
        [
            'Project Summary',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'summary',
                    'project_commit_count',
                    'distribution_count',
                    'total_distribution_count',
                    'lines_of_code',
                    'coding_hours',
                ],
            },
        ],
        [
            'Project Stages',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'distribution_section_stats',
                    'distribution_section_stats_end',
                    'distribution_section_stats_end_summary',
                    'current_stage_section_end_time',
                ],
            },
        ],
        [
            'Visibility and Control',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'publish',
                    'schedule_message',
                ],
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
admin.site.register(Projects, ProjectAdmin)
