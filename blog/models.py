from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from shortuuid.django_fields import ShortUUIDField
from .validate_image import clean_image


# from account.validate_image import clean_image
image_position = (('Left', 'Left'), ('Right', 'Right'))


class Blog(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=15,
        max_length=40,
        alphabet='abcdefg1234',
        primary_key=True,
    )
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from='title',
        unique_with=[
            'date_created',
        ],
    )
    post_summary = models.TextField(max_length=260, help_text='post summary')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # ==============================
    # first blog section
    # ==============================
    first_section_title = models.CharField(
        max_length=200, help_text='section post title', verbose_name='title'
    )
    first_section_summary = models.TextField(
        max_length=300, help_text='section post summary', verbose_name='title summary'
    )
    first_section_post = models.TextField(
        max_length=500, help_text='section post', verbose_name='post'
    )
    first_section_image = models.ImageField(
        upload_to='blog/assets/', validators=[clean_image], verbose_name='image'
    )
    first_section_image_position = models.CharField(
        max_length=10,
        choices=image_position,
        default='Left',
        help_text='image position',
        verbose_name='position',
    )
    first_section_video_link = models.URLField(
        null=False,
        blank=False,
        help_text='video link',
        verbose_name='link',
    )
    first_section_video_description = models.CharField(
        max_length=11,
        help_text='video description',
        verbose_name='desc',
    )
    first_section_list_title_one = models.CharField(
        max_length=20,
        help_text='first description title',
        verbose_name='1st List title',
        default='',
    )
    first_section_list_desc_one = models.TextField(
        max_length=91,
        help_text='description of list title one',
        verbose_name='description',
        default='',
    )

    first_section_list_title_two = models.CharField(
        max_length=20,
        help_text='first description title',
        verbose_name='2nd List title',
        default='',
    )
    first_section_list_desc_two = models.TextField(
        max_length=91,
        help_text='description of list title two',
        verbose_name='description',
        default='',
    )
    first_section_list_title_three = models.CharField(
        max_length=20,
        help_text='first description title',
        verbose_name='3rd List title',
        default='',
    )
    first_section_list_desc_three = models.TextField(
        max_length=91,
        help_text='description of list title three',
        verbose_name='description',
        default='',
    )
    first_section_list_title_four = models.CharField(
        max_length=20,
        help_text='first description title',
        verbose_name='4th List title',
        default='',
    )
    first_section_list_desc_four = models.TextField(
        max_length=91,
        help_text='description of list title four',
        verbose_name='description',
        default='',
    )
    first_section_list_title_five = models.CharField(
        max_length=20,
        help_text='first description title',
        verbose_name='5th List title',
        default='',
    )
    first_section_list_desc_five = models.TextField(
        max_length=91,
        help_text='description of list title five',
        verbose_name='description',
        default='',
    )
    first_section_list_title_six = models.CharField(
        max_length=20,
        help_text='first description title',
        verbose_name='6th List title',
        default='',
    )
    first_section_list_desc_six = models.TextField(
        max_length=91,
        help_text='description of list title six',
        verbose_name='description',
        default='',
    )
    first_section_references = models.TextField(
        max_length=91,
        help_text='section references',
        verbose_name='References',
        null=True,
        blank=True,
    )
    # ==============================
    # second blog section
    # ==============================
    second_section_title = models.CharField(
        max_length=200, help_text='section title', verbose_name='title'
    )
    second_section_summary = models.TextField(
        max_length=300,
        help_text='section post summary',
        verbose_name='summary',
    )
    second_section_post = models.TextField(
        max_length=500,
        help_text='main section post',
        verbose_name='main post',
    )
    second_section_second_post = models.TextField(
        max_length=500,
        help_text='second post of second section',
        verbose_name='secondary post',
    )
    # second_section_short_section_statistic
    second_section_short_stat_name_1 = models.CharField(
        max_length=16,
        help_text='first stats name',
        verbose_name='first stat',
    )
    second_section_short_stat_metric_number_1 = models.IntegerField(
        help_text='first stats metric no',
        verbose_name='stat no',
    )
    second_section_short_stat_name_2 = models.CharField(
        max_length=16,
        help_text='second stats name',
        verbose_name='second stat',
    )
    second_section_short_stat_metric_number_2 = models.IntegerField(
        help_text='second stats metric no',
        verbose_name='stat no',
    )
    second_section_short_stat_name_3 = models.CharField(
        max_length=16,
        help_text='third stats name',
        verbose_name='third stat',
    )
    second_section_short_stat_metric_number_3 = models.IntegerField(
        help_text='third stats metric no',
        verbose_name='stat no',
    )

    # second_section_long_section_statistic
    second_section_long_stat_title = models.CharField(
        max_length=50,
        help_text='long stats name',
        verbose_name='long stat',
    )
    second_section_long_stat_title_metric_number = models.CharField(
        max_length=10,
        help_text='long stats no',
        verbose_name='stat no',
    )
    second_section_long_stat_about_metric = models.TextField(
        max_length=100,
        help_text='about long stats',
        verbose_name='about stat',
    )
    second_section_long_stat_short_name_1 = models.CharField(
        max_length=10, help_text='First short stat name', verbose_name='1st short stat'
    )
    second_section_long_stat_short_metric_number_1 = models.IntegerField(
        help_text='First short stat no',
        verbose_name='stat metric',
    )
    second_section_long_stat_short_stat_name_2 = models.CharField(
        max_length=10, verbose_name='2nd short stat'
    )
    second_section_long_stat_short_metric_number_2 = models.IntegerField(
        help_text='second short stat no', verbose_name='stat metric'
    )
    second_section_long_stat_short_name_3 = models.CharField(
        max_length=10, help_text='Third short stat name', verbose_name='3rd short stat'
    )
    second_section_long_stat_short_metric_number_3 = models.IntegerField(
        help_text='Third short stat name', verbose_name='stat metric'
    )
    second_section_long_stat_short_name_4 = models.CharField(
        max_length=10, help_text='Fourth short stat name', verbose_name='4th short stat'
    )
    second_section_long_stat_short_metric_number_4 = models.IntegerField(
        help_text='Fourth short stat name', verbose_name='stat metric'
    )
    second_section_references = models.TextField(
        max_length=91,
        help_text='section references',
        verbose_name='References',
        null=True,
        blank=True,
    )
    # ==============================
    # third_section
    # ==============================
    third_section_title = models.CharField(
        max_length=200, help_text='section title', verbose_name='title'
    )
    third_section_summary = models.TextField(
        max_length=300, help_text='summary post summary', verbose_name='summary'
    )
    third_section_post = models.TextField(
        max_length=500, help_text='first section post', verbose_name='post'
    )
    third_section_image = models.ImageField(
        upload_to='blog/assets/',
        validators=[clean_image],
        help_text='section image',
        verbose_name='image',
    )
    third_section_image_position = models.CharField(
        max_length=10,
        choices=image_position,
        default='Left',
        help_text='position',
        verbose_name='position',
    )
    third_section_video_link = models.URLField(
        null=False, blank=False, help_text='video link', verbose_name='link'
    )
    third_section_video_description = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        help_text='video description',
        verbose_name='vid Desc',
    )
    # third_section_section_statistic
    third_section_short_stat_1_name = models.CharField(
        max_length=30, help_text='first stat name', verbose_name='1st list title'
    )
    third_section_short_stat_1_description = models.TextField(
        max_length=91, help_text='first stat description', verbose_name='description'
    )
    third_section_short_stat_2_name = models.CharField(
        max_length=30, help_text='second stat name', verbose_name='2nd list title'
    )
    third_section_short_stat_2_description = models.TextField(
        max_length=91, help_text='second stat description', verbose_name='description'
    )
    third_section_short_stat_3_name = models.CharField(
        max_length=30, help_text='third stat name', verbose_name='3rd list title'
    )
    third_section_short_stat_3_description = models.TextField(
        max_length=91, help_text='third stat description', verbose_name='description'
    )
    third_section_short_stat_4_name = models.CharField(
        max_length=30, help_text='fourth stat name', verbose_name='4th list title'
    )
    third_section_short_stat_4_description = models.TextField(
        max_length=91, help_text='fourth stat description', verbose_name='description'
    )
    third_section_short_stat_5_name = models.CharField(
        max_length=30, help_text='fifth stat name', verbose_name='5th list title'
    )
    third_section_short_stat_5_description = models.TextField(
        max_length=91, help_text='fifth stat description', verbose_name='description'
    )
    third_section_short_stat_6_name = models.CharField(
        max_length=30, help_text='sixth stat name', verbose_name='6th list title'
    )
    third_section_short_stat_6_description = models.TextField(
        max_length=91, help_text='sixth stat description', verbose_name='description'
    )
    third_section_references = models.TextField(
        max_length=91,
        help_text='section references',
        verbose_name='References',
        null=True,
        blank=True,
    )
    # ==============================
    # fourth blog section
    # ==============================
    fourth_section_title = models.CharField(
        max_length=200, help_text='section title', verbose_name='title'
    )
    fourth_section_summary = models.TextField(
        max_length=300, help_text='section post summary', verbose_name='summary'
    )
    fourth_section_post = models.TextField(
        max_length=500, help_text='Main post', verbose_name='main post'
    )
    fourth_section_second_post = models.TextField(
        max_length=500, help_text='second post', verbose_name='secondary post'
    )
    # fourth_section_short_section_statistic
    fourth_section_short_stat_name_1 = models.CharField(
        max_length=26, help_text='first stat name', verbose_name='first stat'
    )
    fourth_section_short_stat_metric_number_1 = models.IntegerField(
        help_text='first stat metric no', verbose_name='stat no'
    )
    fourth_section_short_stat_name_2 = models.CharField(
        max_length=26, help_text='second stat name', verbose_name='second stat'
    )
    fourth_section_short_stat_metric_number_2 = models.IntegerField(
        help_text='second stat metric no', verbose_name='stat no'
    )
    fourth_section_short_stat_name_3 = models.CharField(
        max_length=26, help_text='third stat name', verbose_name='third stat'
    )
    fourth_section_short_stat_metric_number_3 = models.IntegerField(
        help_text='third stat metric no', verbose_name='stat no'
    )
    # fourth_section_long_section_statistic
    fourth_section_long_stat_title = models.CharField(
        max_length=30, help_text='long stat title', verbose_name='long stat'
    )
    fourth_section_long_stat_title_metric_number = models.CharField(
        max_length=15, help_text='metric of long title stat', verbose_name='stat no'
    )
    fourth_section_long_stat_about_metric = models.TextField(
        max_length=100, help_text='description of long stats', verbose_name='about stat'
    )
    fourth_section_long_stat_short_name_1 = models.CharField(
        max_length=26, help_text='First short stat name', verbose_name='1st short stat'
    )
    fourth_section_long_stat_short_metric_number_1 = models.IntegerField(
        help_text='First short stat name', verbose_name='stat metric'
    )
    fourth_section_long_stat_short_stat_name_2 = models.CharField(
        max_length=26, help_text='second short stat name', verbose_name='2nd short stat'
    )
    fourth_section_long_stat_short_metric_number_2 = models.IntegerField(
        help_text='Second short stat name', verbose_name='stat metric'
    )
    fourth_section_long_stat_short_name_3 = models.CharField(
        max_length=26, help_text='Third short stat name', verbose_name='3th short stat'
    )
    fourth_section_long_stat_short_metric_number_3 = models.IntegerField(
        help_text='Third short stat name', verbose_name='stat metric'
    )
    fourth_section_long_stat_short_name_4 = models.CharField(
        max_length=26, help_text='Fourth short stat name', verbose_name='4th short stat'
    )
    fourth_section_long_stat_short_metric_number_4 = models.IntegerField(
        help_text='Fourth short stat name', verbose_name='stat metric'
    )
    fourth_section_references = models.TextField(
        max_length=91,
        help_text='section references',
        verbose_name='References',
        null=True,
        blank=True,
    )
    # ==============================
    # fifth section
    # ==============================
    fifth_section_title = models.CharField(
        max_length=200, help_text='section title', verbose_name='title'
    )
    fifth_section_summary = models.TextField(
        max_length=300,
        help_text='section summary',
        verbose_name='summary',
    )
    fifth_section_post = models.TextField(
        max_length=500,
        help_text='section post',
        verbose_name='post',
    )
    fifth_section_image = models.ImageField(
        upload_to='blog/assets/',
        validators=[clean_image],
        verbose_name='Image',
    )
    fifth_section_image_position = models.CharField(
        max_length=10,
        choices=image_position,
        default='Left',
        help_text='image position',
        verbose_name='position',
    )
    fifth_section_video_link = models.URLField(
        null=False, blank=False, help_text='video link', verbose_name='link'
    )
    fifth_section_video_description = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        help_text='video description',
        verbose_name='desc',
    )
    # fifth_section_section_statistic
    fifth_section_short_stat_1_name = models.CharField(
        max_length=30,
        help_text='first description title',
        verbose_name='1st List title',
    )
    fifth_section_short_stat_1_description = models.TextField(
        max_length=91,
        help_text='description of list title one',
        verbose_name='description',
    )
    fifth_section_short_stat_2_name = models.CharField(
        max_length=30,
        help_text='second description title',
        verbose_name='2nd List title',
    )
    fifth_section_short_stat_2_description = models.TextField(
        max_length=91,
        help_text='description of list title two',
        verbose_name='description',
    )
    fifth_section_short_stat_3_name = models.CharField(
        max_length=30,
        help_text='third description title',
        verbose_name='3rd List title',
    )
    fifth_section_short_stat_3_description = models.TextField(
        max_length=91,
        help_text='description of list title three',
        verbose_name='description',
    )
    fifth_section_short_stat_4_name = models.CharField(
        max_length=30,
        help_text='fourth description title',
        verbose_name='4th List title',
    )
    fifth_section_short_stat_4_description = models.TextField(
        max_length=91,
        help_text='description of list title four',
        verbose_name='description',
    )
    fifth_section_short_stat_5_name = models.CharField(
        max_length=30,
        help_text='fifth description title',
        verbose_name='5th List title',
    )
    fifth_section_short_stat_5_description = models.TextField(
        max_length=91,
        help_text='description of list title five',
        verbose_name='description',
    )
    fifth_section_short_stat_6_name = models.CharField(
        max_length=30,
        help_text='sixth description title',
        verbose_name='6th List title',
    )
    fifth_section_short_stat_6_description = models.TextField(
        max_length=91,
        help_text='description of list title six',
        verbose_name='description',
    )
    fifth_section_references = models.TextField(
        max_length=91,
        help_text='section references',
        verbose_name='References',
        null=True,
        blank=True,
    )
    # ==============================
    # others
    # ==============================
    publish = models.BooleanField(default=True)
    schedule_message = models.DateTimeField(
        default=timezone.now,
        help_text='Schedule when this post should become visible to author. \
            <span style="font-weight:bold;">Note: Publish post must be ticked for this to work</span>',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=timezone.now)
    # track views
    number_of_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'

    def get_absolute_url(self):
        return reverse('blog_details', kwargs={'id': self.id, 'slug': self.slug})
