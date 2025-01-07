from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_prose_editor.fields import ProseEditorField
from multiselectfield import MultiSelectField
from shortuuid.django_fields import ShortUUIDField
from simple_history.models import HistoricalRecords

from .utils.validate_image import clean_image

category = (
    ('Research', 'Research'),
    ('Innovation', 'Innovation'),
    ('Webinar', 'Webinar'),
    ('Showcase', 'Showcase'),
    ('Funding', 'Funding'),
    ('News/Events', 'News/Events'),
)


class Blog(models.Model):
    post_id = ShortUUIDField(length=12, max_length=15, alphabet='aghrsdfg1234', editable=False, primary_key=True)
    title = models.CharField(max_length=65, help_text='enter post title')
    slug = AutoSlugField(populate_from='title', unique_with=['post_id'])
    author = models.CharField(max_length=200)
    category = MultiSelectField(choices=category, default='Research', max_length=100)
    post_one = ProseEditorField(max_length=1700)
    post_two = ProseEditorField(max_length=960, null=True, blank=True)
    post_three = ProseEditorField(max_length=960, null=True, blank=True)
    tags = models.CharField(max_length=500)
    featured_image = models.ImageField(upload_to='blog/images', validators=[clean_image])
    facebook = models.URLField(null=True, blank=True, help_text='facebook post link')
    twitter = models.URLField(null=True, blank=True, help_text='twitter post link')
    linkedin = models.URLField(null=True, blank=True, help_text='linkedin post link', verbose_name='LinkedIn')
    gallery_image_1 = models.ImageField(
        upload_to='blog/images', validators=[clean_image], help_text='additional blog images'
    )
    gallery_image_2 = models.ImageField(
        upload_to='blog/images', validators=[clean_image], help_text='additional blog images'
    )
    gallery_image_3 = models.ImageField(
        upload_to='blog/images', validators=[clean_image], help_text='additional blog images'
    )
    views_count = models.IntegerField(default=0)
    publish = models.BooleanField(default=True)
    date_published = models.DateTimeField(auto_now_add=True)
    schedule_publish = models.DateTimeField(
        default=timezone.now,
        help_text='Schedule when this post should become visible on the site. \
                            <span style="color:red;">Note: Publish must be ticked for this to work</span>'
    )
    history = HistoricalRecords(inherit=True)
    date_updated = models.DateTimeField(
        default=timezone.now, verbose_name='Update Date/Time', help_text='dated last updated'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_published']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'

    def get_absolute_url(self):
        return reverse('blog_details', kwargs={'id': self.id, 'slug': self.slug})
