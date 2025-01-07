from autoslug import AutoSlugField
from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField

from core.bootcamps.utils.modelChoices import nationality
from core.events.models import EventBase

level = (
    ('Higher Certificate', 'Higher Certificate'),
    ('Diploma', 'Diploma'),
    ('Year 1', 'Year 1'),
    ('Year 2', 'Year 2'),
    ('Year 3', 'Year 3'),
    ('Year 4', 'Year 4'),
    ('Honours', 'Honours'),
    ('Post Graduate', 'Post Graduate'),
    ('Others', 'Others'),
)

applicant_selection = (
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
)

gender = (
    ('Female', 'Female'),
    ('Male', 'Male'),
)


class ProgramConfig(EventBase):
    event_title = models.CharField(max_length=200)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.event_title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Program Config'
        verbose_name_plural = 'Program Configs'


class ProgramSignUp(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=50, choices=gender, default='Female')
    nationality = models.CharField(max_length=50, choices=nationality, default='South Africa')
    phone_number = models.CharField(max_length=30, default='')
    organization = models.CharField(max_length=300, default='University of Johannesburg')
    expectation = models.TextField(max_length=800)
    application_status = models.CharField(null=True, blank=True, choices=applicant_selection)
    program_settings = models.ForeignKey(
        'ProgramConfig', on_delete=models.CASCADE, null=True, blank=True, help_text='program settings'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Program Signup'
        verbose_name_plural = 'Program Signup'


class ProjectBuild(models.Model):
    project_id = ShortUUIDField(length=16, max_length=40, alphabet='abcdefg1234', primary_key=True)
    title = models.CharField(max_length=200, help_text='project tile')
    slug = AutoSlugField(populate_from='title', unique_with=['date_created'])
    summary = models.TextField(max_length=500, help_text='about project')
    project_progress = models.IntegerField(help_text='project progress')
    project_commit_count = models.IntegerField(help_text='project commit count')
    distribution_count = models.IntegerField(help_text='project distribution')
    total_distribution_count = models.IntegerField(help_text='total project distribution')
    lines_of_code = models.IntegerField(help_text='project lines of code')
    coding_hours = models.IntegerField(help_text='project coding hours')
    distribution_section_stats = models.CharField(max_length=100, help_text='distribution section count')
    distribution_section_stats_end = models.CharField(max_length=100, help_text='distribution end section count')
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
                                <span style="font-weight:bold;">Note: Publish post must be \
                                ticked for this to work</span>',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
