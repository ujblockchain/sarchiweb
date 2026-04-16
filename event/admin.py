from django.contrib import admin
from import_export import resources
from .models import EventRegistration, FewsRegistration
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import messages


class EventResource(resources.ModelResource):
    class Meta:
        model = EventRegistration
        chunk_size = 300

    def get_queryset(self):
        return super().get_queryset().select_related()

    def filter_export(self, queryset, **kwargs):
        return queryset


@admin.register(EventRegistration)
class EventApplicationAdmin(ImportExportActionModelAdmin):
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
    list_filter = ['status']
    date_hierarchy = 'created_at'
    list_per_page = 10
    actions_on_top = True
    readonly_fields = ['id', 'created_at']
    save_as = True
    save_as_continue = True
    actions_on_top = True
    actions_on_bottom = True
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'faculty',
        'department',
        'status',
    ]
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

    @admin.action(description="Mark as selected", permissions=['change'])
    def make_selected(self, request, queryset):
        # mark selected applications as selected
        count = 0
        for obj in queryset.iterator():
            if obj.status != 'selected':
                obj.status = 'selected'
                obj.save(update_fields=['status'])
                count += 1

        self.message_user(
            request,
            f"{count} application(s) successfully marked as selected.",
            messages.SUCCESS,
        )

    @admin.action(description="Mark as rejected", permissions=['change'])
    def make_rejected(self, request, queryset):
        # mark selected applications as rejected
        count = 0
        for obj in queryset.iterator():
            if obj.status != 'rejected':
                obj.status = 'rejected'
                obj.save(update_fields=['status'])
                count += 1

        self.message_user(
            request,
            f"{count} application(s) successfully marked as rejected.",
            messages.ERROR,
        )

    @admin.display(description='Status', ordering='status')
    def status_display(self, obj):
        if obj.status == 'selected':
            return "Selected"
        elif obj.status == 'rejected':
            return "Rejected"
        return "Pending"

    actions = ['make_selected', 'make_rejected']


@admin.register(FewsRegistration)
class FewsApplicationAdmin(ImportExportActionModelAdmin):
    resource_classes = [EventResource]
    list_display = [
        'first_name',
        'last_name',
        'organization',
        'attendance_type',
        'created_at',
        'status_display',
    ]
    list_display_links = ['first_name', 'last_name', 'organization', 'attendance_type']
    list_filter = ['status', 'attendance_type']
    date_hierarchy = 'created_at'
    list_per_page = 10
    actions_on_top = True
    readonly_fields = ['id', 'created_at']
    save_as = True
    save_as_continue = True
    actions_on_top = True
    actions_on_bottom = True
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'organization',
        'attendance_type',
        'status',
    ]
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

    @admin.action(description="Mark as selected", permissions=['change'])
    def make_selected(self, request, queryset):
        # mark selected applications as selected
        count = 0
        for obj in queryset.iterator():
            if obj.status != 'selected':
                obj.status = 'selected'
                obj.save(update_fields=['status'])
                count += 1

        self.message_user(
            request,
            f"{count} application(s) successfully marked as selected.",
            messages.SUCCESS,
        )

    @admin.action(description="Mark as rejected", permissions=['change'])
    def make_rejected(self, request, queryset):
        # mark selected applications as rejected
        count = 0
        for obj in queryset.iterator():
            if obj.status != 'rejected':
                obj.status = 'rejected'
                obj.save(update_fields=['status'])
                count += 1

        self.message_user(
            request,
            f"{count} application(s) successfully marked as rejected.",
            messages.ERROR,
        )

    @admin.display(description='Status', ordering='status')
    def status_display(self, obj):
        if obj.status == 'selected':
            return "Selected"
        elif obj.status == 'rejected':
            return "Rejected"
        return "Pending"

    actions = ['make_selected', 'make_rejected']
