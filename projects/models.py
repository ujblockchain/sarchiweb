from django.db import models
from django.utils import timezone
from autoslug import AutoSlugField
from shortuuid.django_fields import ShortUUIDField


class Projects(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
        primary_key=True,
    )
    title = models.CharField(max_length=200, help_text='project tile')
    slug = AutoSlugField(
        populate_from='title',
        unique_with=[
            'date_created',
        ],
    )
    summary = models.TextField(max_length=500, help_text='about project')
    project_progress = models.IntegerField(help_text='project progress')
    project_commit_count = models.IntegerField(help_text='project commit count')
    distribution_count = models.IntegerField(help_text='project distribution')
    total_distribution_count = models.IntegerField(help_text='total project distribution')
    lines_of_code = models.IntegerField(help_text='project lines of code')
    coding_hours = models.IntegerField(help_text='project coding hours')
    distribution_section_stats = models.CharField(
        max_length=100, help_text='distribution section count'
    )
    distribution_section_stats_end = models.CharField(
        max_length=100, help_text='distribution end section count'
    )
    distribution_section_stats_end_summary = models.TextField(
        max_length=500, help_text='short summary on project phases'
    )
    current_stage_section_end_time = models.DateTimeField()
    project_start_time = models.DateTimeField()
    project_end_time = models.DateTimeField()
    publish = models.BooleanField(default=True)
    schedule_message = models.DateTimeField(
        default=timezone.now,
        help_text='Schedule when this post should become visible to author. \
                                <span style="font-weight:bold;">Note: Publish post must be ticked for this to work</span>',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
