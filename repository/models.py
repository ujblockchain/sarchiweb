from django.db import models
from django.utils import timezone


class RepoInfo(models.Model):
    active_repo = models.URLField()
    total_repo = models.IntegerField()
    total_commit = models.IntegerField(default=100)
    sha = models.CharField(max_length=300, default='', help_text='last commit sha recorded')
    last_commit_time = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.active_repo

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Repository"
        verbose_name_plural = "Repository"
