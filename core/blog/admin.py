from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, utc
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Blog


@admin.display(description='Publish/Unpublish Selection')
def visibility_action(modeladmin, request, querryset):
    if querryset.filter(publish=True):
        querryset.update(publish=False)
        messages.add_message(request, messages.SUCCESS, 'selected list unpublished successfully')
    else:
        querryset.update(publish=True)
        messages.add_message(request, messages.SUCCESS, 'selected list published successfully')


class BlogResource(resources.ModelResource):

    class Meta:
        model = Blog
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['post_id']


class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = BlogResource
    list_display = ['post_id', 'title', 'author', 'category', 'publish', 'schedule_post', 'date_updated']
    list_display_links = ['title', 'author', 'category', 'date_updated']
    list_editable = ['publish']
    list_filter = ['publish']
    search_fields = ['title', 'author', 'category', 'post', 'tags', 'publish', 'date_updated']
    date_hierarchy = 'date_updated'
    list_per_page = 50
    show_full_result_count = True
    actions = [visibility_action]
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    view_on_site = True
    fieldsets = [
        ['Info', {
            'classes': ['wide', 'extrapretty'],
            'fields': ['title', 'author', 'category', 'tags']
        }],
        [
            'Details', {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['post_one', 'post_two', 'post_three']
            }
        ],
        ['Social', {
            'classes': ['collapse', 'wide', 'extrapretty'],
            'fields': ['facebook', 'twitter', 'linkedin']
        }],
        [
            'Media', {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': [
                    'featured_image',
                    'gallery_image_1',
                    'gallery_image_2',
                    'gallery_image_3',
                ]
            }
        ],
        [
            'Visibility', {
                'classes': ['collapse', 'wide', 'extrapretty'],
                'fields': ['publish', 'schedule_publish', 'date_updated']
            }
        ],
    ]

    @admin.display(description='Post Schedule')
    def schedule_post(self, obj):
        if obj.schedule_publish > datetime.now().replace(tzinfo=utc):
            return format_html(
                '<span style="color:white; background:#DD3438; font-size:14px; padding: 5px 8px; border:1px solid red; border-radius:10px;">*Yes</span>'  # noqa: E501
            )
        else:
            return format_html(
                '<span style="color:#453F3F; font-weight:bolder; background:#CBCBCB; font-size:14px; padding: 5px 8px; border:1px solid #453F3F; border-radius:10px;">*No</span>'  # noqa: E501
            )

    # override field
    def formfield_for_dbfield(self, db_field, request, **kwargs):  # noqa: E301

        if db_field.name == 'category':
            # redeclare label with a class
            label = mark_safe(
                f'<label class="font-medium mb-2 text-gray-900 text-sm dark:text-gray-200">{db_field.verbose_name}</label>'  # noqa: E501
            )
            # Override the status field to use MultipleChoiceField with SelectMultiple widget
            kwargs['widget'] = forms.SelectMultiple(
                attrs={
                    'class':
                        'border bg-white font-medium min-w-20 rounded-md shadow-sm text-gray-500 text-sm focus:ring focus:ring-primary-300 focus:border-primary-600 focus:outline-none group-[.errors]:border-red-600 group-[.errors]:focus:ring-red-200 dark:bg-gray-900 dark:border-gray-700 dark:text-gray-400 dark:focus:border-primary-600 dark:focus:ring-primary-700 dark:focus:ring-opacity-50 dark:group-[.errors]:border-red-500 dark:group-[.errors]:focus:ring-red-600/40 px-3 py-2 w-full pr-8 max-w-2xl appearance-none',  # noqa: E501
                    'style':
                        'height: 120px;'  # Set the height for the select field
                }
            )
            kwargs['choices'] = [('Research', 'Research'), ('Innovation', 'Innovation'), ('Webinar', 'Webinar'),
                                 ('Showcase', 'Showcase'), ('Funding', 'Funding'), ('News/Events', 'News/Events')]
            kwargs['label'] = label
            kwargs['help_text'] = db_field.help_text
            kwargs['initial'] = ['Research']

            return forms.MultipleChoiceField(**kwargs)
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# noqa: E305
admin.site.register(Blog, BlogAdmin)
