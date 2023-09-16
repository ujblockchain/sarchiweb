from django.contrib import admin
from .models import RepoInfo


class RepoAdmin(admin.ModelAdmin):
    list_display = [
        'active_repo',
        'total_repo',
        'total_commit',
        'timestamp',
    ]
    list_display_links = [
        'active_repo',
        'total_repo',
        'total_commit',
    ]
    search_fields = [
        'active_repo',
        'total_repo',
        'total_commit',
        'timestamp',
    ]
    list_per_page = 50
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    readonly_fields = [
        'sha',
        'node_id',
    ]
    fields = [
        'active_repo',
        'total_repo',
        'total_commit',
        'sha',
        'node_id',
        'timestamp',
    ]


#
admin.site.register(RepoInfo, RepoAdmin)
