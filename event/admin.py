from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import messages
from rangefilter.filters import DateRangeFilterBuilder

from event.utils import send_bulk_status_email, send_single_status_email
from .models import EventEmailConfig, EventRegistration, FewsRegistration


class EventResource(resources.ModelResource):
    class Meta:
        model = EventRegistration
        chunk_size = 100


class FewsResource(resources.ModelResource):
    class Meta:
        model = FewsRegistration
        chunk_size = 100


class StatusManagementMixin:

    @admin.display(description='Status', ordering='status')
    def status_display(self, obj):
        status_map = {'selected': "Selected", 'rejected': "Rejected"}
        return status_map.get(obj.status, "Pending")

    #  opening a single record and clicking save
    def save_model(self, request, obj, form, change):
        # save the model to the database normally
        super().save_model(request, obj, form, change)

        # if an existing record change (change=true) and the status was modified
        if change and 'status' in form.changed_data:
            send_single_status_email(obj, obj.status)
            self.message_user(
                request,
                f"Status updated to {obj.status} and email sent to {obj.email}.",
                messages.SUCCESS,
            )

    # selecting multiple records via bulk actions
    @admin.action(description="Mark as selected")
    def make_selected(self, request, queryset):
        target_qs = queryset.exclude(status='selected')
        bcc_emails = list(target_qs.values_list('email', flat=True))

        if bcc_emails:
            updated = target_qs.update(status='selected')
            send_bulk_status_email(self.model, bcc_emails, status='selected')
            self.message_user(
                request,
                f"{updated} application(s) successfully marked as selected and emailed.",
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request, "No eligible applications to update.", messages.WARNING
            )

    @admin.action(description="Mark as rejected")
    def make_rejected(self, request, queryset):
        target_qs = queryset.exclude(status='rejected')
        bcc_emails = list(target_qs.values_list('email', flat=True))

        if bcc_emails:
            updated = target_qs.update(status='rejected')
            send_bulk_status_email(self.model, bcc_emails, status='rejected')
            self.message_user(
                request,
                f"{updated} application(s) successfully marked as rejected and emailed.",
                messages.ERROR,
            )
        else:
            self.message_user(
                request, "No eligible applications to update.", messages.WARNING
            )


@admin.register(EventEmailConfig)
class EventConfigAdmin(admin.ModelAdmin):
    list_display = [
        'event_type',
        'group_link',
        'created_at',
    ]
    list_display_links = ['event_type', 'group_link']
    list_filter = ['event_type']
    date_hierarchy = 'created_at'
    list_per_page = 10
    search_fields = ['event_type']
    readonly_fields = ['id', 'created_at']
    save_as = True

    fieldsets = [
        [
            'Event Type',
            {'fields': ['event_type']},
        ],
        [
            'Email Template for Application',
            {
                'classes': ['collasible', 'wide'],
                'fields': [
                    'applied_subject',
                    'applied_message_text',
                ],
            },
        ],
        [
            'Email Template for Selection',
            {
                'classes': ['collasible', 'wide'],
                'fields': [
                    'selected_subject',
                    'selected_message_text',
                    'selected_bulk_message_text',
                ],
            },
        ],
        [
            'Email Template for Rejection',
            {
                'classes': ['collasible', 'wide'],
                'fields': [
                    'rejected_subject',
                    'rejected_message_text',
                    'rejected_bulk_message_text',
                ],
            },
        ],
        [
            'Other Details',
            {
                'classes': ['collasible', 'wide'],
                'fields': ['group_link', 'attachment', 'registration_end_time'],
            },
        ],
        [
            'Important dates',
            {'classes': ['collasible', 'wide'], 'fields': ['created_at']},
        ],
    ]


@admin.register(EventRegistration)
class EventApplicationAdmin(StatusManagementMixin, ImportExportActionModelAdmin):
    resource_classes = [EventResource]
    list_display = [
        'first_name',
        'last_name',
        'faculty',
        'department',
        'created_at',
        'status_display',
    ]
    list_display_links = ['first_name', 'last_name', 'faculty', 'department']
    list_filter = (
        'status',
        ("created_at", DateRangeFilterBuilder()),
    )
    list_per_page = 30
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'faculty',
        'department',
        'status',
    ]
    readonly_fields = ['id', 'created_at']
    save_as = True
    actions_on_top = True
    actions_on_bottom = True
    actions = ['make_selected', 'make_rejected']

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


@admin.register(FewsRegistration)
class FewsApplicationAdmin(StatusManagementMixin, ImportExportActionModelAdmin):
    resource_classes = [FewsResource]
    list_display = [
        'first_name',
        'last_name',
        'organization',
        'attendance_type',
        'created_at',
        'status_display',
    ]
    list_display_links = ['first_name', 'last_name', 'organization', 'attendance_type']
    list_filter = (
        'status',
        'attendance_type',
        ("created_at", DateRangeFilterBuilder()),
    )
    list_per_page = 30
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'organization',
        'attendance_type',
        'status',
    ]
    readonly_fields = ['id', 'created_at']
    save_as = True
    actions_on_top = True
    actions_on_bottom = True
    actions = ['make_selected', 'make_rejected']

    fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'organization',
        'attendance_type',
        'status',
        'created_at',
    ]
