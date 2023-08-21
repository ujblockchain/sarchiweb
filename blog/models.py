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
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
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
    first_section_title = models.CharField(max_length=200, help_text='section post title')
    first_section_summary = models.TextField(max_length=300, help_text='section post summary')
    first_section_post = models.TextField(max_length=500, help_text='section post')
    first_section_image = models.ImageField(upload_to='blog/assets/', validators=[clean_image])
    first_section_image_position = models.CharField(
        max_length=10, choices=image_position, default='Left'
    )
    first_section_video_link = models.URLField(null=False, blank=False)
    first_section_video_description = models.CharField(max_length=11)
    first_section_list_per_desc = models.TextField(
        max_length=91, help_text='description on per to per features of tech written in the post'
    )
    first_section_list_borderless_application_desc = models.TextField(
        max_length=91, help_text='borderless application of tech written in the post'
    )
    first_section_list_platform_security_desc = models.TextField(
        max_length=91, help_text='platform immutability of tech written in the post'
    )
    first_section_list_contract_desc = models.TextField(
        max_length=91, help_text='smart contract application of tech written in the post'
    )
    first_section_list_ledger_desc = models.TextField(
        max_length=91, help_text='decentralized ledger application of tech written in the post'
    )
    first_section_use_case_desc = models.TextField(
        max_length=91, help_text='use case of  tech in post to Agri-food'
    )
    # ==============================
    # second blog section
    # ==============================
    second_section_title = models.CharField(max_length=200)
    second_section_summary = models.TextField(max_length=300, help_text='section post summary')
    second_section_post = models.TextField(max_length=500, help_text='second section post')
    second_section_second_post = models.TextField(
        max_length=500, help_text='second post of second section'
    )
    # second_section_short_section_statistic
    second_section_short_stat_name_1 = models.CharField(max_length=16, help_text='first stats name')
    second_section_short_stat_metric_number_1 = models.IntegerField(
        help_text='first stats metric no'
    )
    second_section_short_stat_name_2 = models.CharField(
        max_length=16, help_text='second stats name'
    )
    second_section_short_stat_metric_number_2 = models.IntegerField(
        help_text='second stats metric no'
    )
    second_section_short_stat_name_3 = models.CharField(max_length=16, help_text='third stats name')
    second_section_short_stat_metric_number_3 = models.IntegerField(
        help_text='third stats metric no'
    )

    # second_section_long_section_statistic
    second_section_long_stat_title = models.CharField(max_length=50)
    second_section_long_stat_title_metric_number = models.CharField(max_length=10)
    second_section_long_stat_about_metric = models.TextField(max_length=100)
    second_section_long_stat_short_name_1 = models.CharField(max_length=10)
    second_section_long_stat_short_metric_number_1 = models.IntegerField()
    second_section_long_stat_short_stat_name_2 = models.CharField(max_length=10)
    second_section_long_stat_short_metric_number_2 = models.IntegerField()
    second_section_long_stat_short_name_3 = models.CharField(max_length=10)
    second_section_long_stat_short_metric_number_3 = models.IntegerField()
    second_section_long_stat_short_name_4 = models.CharField(max_length=10)
    second_section_long_stat_short_metric_number_4 = models.IntegerField()
    # ==============================
    # third_section
    # ==============================
    third_section_title = models.CharField(max_length=200)
    third_section_summary = models.TextField(max_length=300, help_text='summary post summary')
    third_section_post = models.TextField(max_length=500, help_text='first section post')
    third_section_image = models.ImageField(upload_to='blog/assets/', validators=[clean_image])
    third_section_image_position = models.CharField(
        max_length=10, choices=image_position, default='Left'
    )
    third_section_video_link = models.URLField(null=False, blank=False)
    third_section_video_description = models.CharField(max_length=15, null=False, blank=False)
    # third_section_section_statistic
    third_section_short_stat_1_name = models.CharField(max_length=30, help_text='first stat name')
    third_section_short_stat_1_description = models.TextField(
        max_length=91, help_text='first stat description'
    )
    third_section_short_stat_2_name = models.CharField(max_length=30, help_text='second stat name')
    third_section_short_stat_2_description = models.TextField(
        max_length=91, help_text='second stat description'
    )
    third_section_short_stat_3_name = models.CharField(max_length=30, help_text='third stat name')
    third_section_short_stat_3_description = models.TextField(
        max_length=91, help_text='third stat description'
    )
    third_section_short_stat_4_name = models.CharField(max_length=30, help_text='fourth stat name')
    third_section_short_stat_4_description = models.TextField(
        max_length=91, help_text='fourth stat description'
    )
    third_section_short_stat_5_name = models.CharField(max_length=30, help_text='fifth stat name')
    third_section_short_stat_5_description = models.TextField(
        max_length=91, help_text='fifth stat description'
    )
    third_section_short_stat_6_name = models.CharField(max_length=30, help_text='sixth stat name')
    third_section_short_stat_6_description = models.TextField(
        max_length=91, help_text='sixth stat description'
    )
    # ==============================
    # fourth blog section
    # ==============================
    fourth_section_title = models.CharField(max_length=200)
    fourth_section_summary = models.TextField(max_length=300, help_text='section post summary')
    fourth_section_post = models.TextField(max_length=500, help_text='fourth section post')
    fourth_section_second_post = models.TextField(
        max_length=500, help_text='second post of fourth section'
    )
    # fourth_section_short_section_statistic
    fourth_section_short_stat_name_1 = models.CharField(
        max_length=26, help_text='first stat name'
    )
    fourth_section_short_stat_metric_number_1 = models.IntegerField(
        help_text='first stat metric no'
    )
    fourth_section_short_stat_name_2 = models.CharField(
        max_length=26, help_text='second stat name'
    )
    fourth_section_short_stat_metric_number_2 = models.IntegerField(
        help_text='second stat metric no'
    )
    fourth_section_short_stat_name_3 = models.CharField(
        max_length=26, help_text='third stat name'
    )
    fourth_section_short_stat_metric_number_3 = models.IntegerField(
        help_text='third stat metric no'
    )
    # fourth_section_long_section_statistic
    fourth_section_long_stat_title = models.CharField(max_length=30, help_text='title of stat')
    fourth_section_long_stat_title_metric_number = models.CharField(
        max_length=15, help_text='metric backing the title stat'
    )
    fourth_section_long_stat_about_metric = models.TextField(
        max_length=100, help_text='description of title stats'
    )
    fourth_section_long_stat_short_name_1 = models.CharField(
        max_length=26, help_text='long first stat name'
    )
    fourth_section_long_stat_short_metric_number_1 = models.IntegerField(
        help_text='long first stat metric number'
    )
    fourth_section_long_stat_short_stat_name_2 = models.CharField(
        max_length=26, help_text='long second stat name'
    )
    fourth_section_long_stat_short_metric_number_2 = models.IntegerField(
        help_text='long second stat metric number'
    )
    fourth_section_long_stat_short_name_3 = models.CharField(
        max_length=26, help_text='long third stat name'
    )
    fourth_section_long_stat_short_metric_number_3 = models.IntegerField(
        help_text='long third stat metric number'
    )
    fourth_section_long_stat_short_name_4 = models.CharField(
        max_length=26, help_text='long fourth stat name'
    )
    fourth_section_long_stat_short_metric_number_4 = models.IntegerField(
        help_text='long fourth stat metric number'
    )
    # ==============================
    # fifth section
    # ==============================
    fifth_section_title = models.CharField(max_length=200)
    fifth_section_summary = models.TextField(
        max_length=300, help_text='an intro that give an idea of the tile'
    )
    fifth_section_post = models.TextField(max_length=500, help_text='first section post')
    fifth_section_image = models.ImageField(upload_to='blog/assets/', validators=[clean_image])
    fifth_section_image_position = models.CharField(
        max_length=10, choices=image_position, default='Left'
    )
    fifth_section_video_link = models.URLField(null=False, blank=False)
    fifth_section_video_description = models.CharField(max_length=15, null=False, blank=False)
    # fifth_section_section_statistic
    fifth_section_short_stat_1_name = models.CharField(max_length=30, help_text='first stat name')
    fifth_section_short_stat_1_description = models.TextField(
        max_length=91, help_text='first stat description'
    )
    fifth_section_short_stat_2_name = models.CharField(max_length=30, help_text='second stat name')
    fifth_section_short_stat_2_description = models.TextField(
        max_length=91, help_text='second stat description'
    )
    fifth_section_short_stat_3_name = models.CharField(max_length=30, help_text='third stat name')
    fifth_section_short_stat_3_description = models.TextField(
        max_length=91, help_text='third stat description'
    )
    fifth_section_short_stat_4_name = models.CharField(max_length=30, help_text='fourth stat name')
    fifth_section_short_stat_4_description = models.TextField(
        max_length=91, help_text='fourth stat description'
    )
    fifth_section_short_stat_5_name = models.CharField(max_length=30, help_text='fifth stat name')
    fifth_section_short_stat_5_description = models.TextField(
        max_length=91, help_text='fifth stat description'
    )
    fifth_section_short_stat_6_name = models.CharField(max_length=30, help_text='sixth stat name')
    fifth_section_short_stat_6_description = models.TextField(
        max_length=91, help_text='sixth stat description'
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
