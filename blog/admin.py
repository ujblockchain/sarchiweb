from django.contrib import admin
from django.contrib import messages
from .models import Blog


def visibility_action(modeladmin, request, querryset):
    if querryset.filter(publish=True):
        querryset.update(publish=False)
        messages.add_message(request, messages.SUCCESS, 'selected list publish changed')
    else:
        querryset.update(publish=True)
        messages.add_message(request, messages.SUCCESS, 'selected list publish changed')


visibility_action.short_description = 'hide/show selection'


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author',
        'first_section_title',
        'second_section_title',
        'third_section_title',
        'fourth_section_title',
        'fifth_section_title',
        'number_of_views',
        'publish',
        'schedule_message',
        'last_update',
    ]
    list_display_links = [
        'id',
        'title',
        'first_section_title',
        'second_section_title',
        'third_section_title',
        'fourth_section_title',
        'fifth_section_title',
        'number_of_views',
    ]
    list_filter = [
        'first_section_image_position',
        'third_section_image_position',
        'fifth_section_image_position',
        'publish',
    ]
    search_fields = [
        'title',
        'author',
        'first_section_title',
        'second_section_title',
        'third_section_title',
        'fourth_section_title',
        'fifth_section_title',
        'number_of_views',
    ]
    readonly_fields = ['id', 'slug', 'number_of_views',]
    list_per_page = 50
    view_on_site = True
    show_full_result_count = True
    actions = [visibility_action]
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fieldsets = [
        ['General Information', {'classes': ['wide'], 'fields': ['id', 'author']}],
        [
            'Blog Summary',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'title',
                    'post_summary',
                ],
            },
        ],
        [
            'First Section',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'first_section_title',
                    'first_section_summary',
                    'first_section_post',
                    'first_section_image',
                    'first_section_image_position',
                    'first_section_video_link',
                    'first_section_video_description',
                    'first_section_list_per_desc',
                    'first_section_list_borderless_application_desc',
                    'first_section_list_platform_security_desc',
                    'first_section_list_contract_desc',
                    'first_section_list_ledger_desc', 
                    'first_section_use_case_desc',
                ],
            },
        ],
        [
            'Second Section',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'second_section_title',
                    'second_section_summary',
                    'second_section_post',
                    'second_section_second_post',
                    'second_section_short_stat_name_1',
                    'second_section_short_stat_metric_number_1',
                    'second_section_short_stat_name_2',
                    'second_section_short_stat_metric_number_2',
                    'second_section_short_stat_name_3',
                    'second_section_short_stat_metric_number_3',
                    'second_section_long_stat_title',
                    'second_section_long_stat_title_metric_number',
                    'second_section_long_stat_about_metric',
                    'second_section_long_stat_short_name_1',
                    'second_section_long_stat_short_metric_number_1',
                    'second_section_long_stat_short_stat_name_2',
                    'second_section_long_stat_short_metric_number_2',
                    'second_section_long_stat_short_name_3',
                    'second_section_long_stat_short_metric_number_3',
                    'second_section_long_stat_short_name_4',
                    'second_section_long_stat_short_metric_number_4',

                ],
            },
        ],
        [
            'Third Section',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'third_section_title',
                    'third_section_summary',
                    'third_section_post',
                    'third_section_image',
                    'third_section_image_position',
                    'third_section_video_link',
                    'third_section_video_description',
                    'third_section_short_stat_1_name',
                    'third_section_short_stat_1_description',
                    'third_section_short_stat_2_name',
                    'third_section_short_stat_2_description',
                    'third_section_short_stat_3_name',
                    'third_section_short_stat_3_description',
                    'third_section_short_stat_4_name',
                    'third_section_short_stat_4_description',
                    'third_section_short_stat_5_name',
                    'third_section_short_stat_5_description',
                    'third_section_short_stat_6_name',
                    'third_section_short_stat_6_description',
                ],
            },
        ],
        [
            'Fourth Section',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'fourth_section_title',
                    'fourth_section_summary',
                    'fourth_section_post',
                    'fourth_section_second_post',
                    'fourth_section_short_stat_name_1',
                    'fourth_section_short_stat_metric_number_1',
                    'fourth_section_short_stat_name_2',
                    'fourth_section_short_stat_metric_number_2',
                    'fourth_section_short_stat_name_3',
                    'fourth_section_short_stat_metric_number_3',
                    'fourth_section_long_stat_title',
                    'fourth_section_long_stat_title_metric_number',
                    'fourth_section_long_stat_about_metric',
                    'fourth_section_long_stat_short_name_1',
                    'fourth_section_long_stat_short_metric_number_1',
                    'fourth_section_long_stat_short_stat_name_2',
                    'fourth_section_long_stat_short_metric_number_2',
                    'fourth_section_long_stat_short_name_3',
                    'fourth_section_long_stat_short_metric_number_3',
                    'fourth_section_long_stat_short_name_4',
                    'fourth_section_long_stat_short_metric_number_4',

                ],
            },
        ],
        [
            'Fifth Section',
            {
                'classes': ['collapse', 'wide'],
                'fields': [
                    'fifth_section_title',
                    'fifth_section_summary',
                    'fifth_section_post',
                    'fifth_section_image', 
                    'fifth_section_image_position',
                    'fifth_section_video_link',
                    'fifth_section_video_description',
                    'fifth_section_short_stat_1_name', 
                    'fifth_section_short_stat_2_name',
                    'fifth_section_short_stat_1_description',
                    'fifth_section_short_stat_2_description',
                    'fifth_section_short_stat_3_name', 
                    'fifth_section_short_stat_4_name',
                    'fifth_section_short_stat_3_description',
                    'fifth_section_short_stat_4_description',
                    'fifth_section_short_stat_5_name', 
                    'fifth_section_short_stat_6_name',
                    'fifth_section_short_stat_5_description',
                    'fifth_section_short_stat_6_description',

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


# register model in admin
admin.site.register(Blog, BlogAdmin)
