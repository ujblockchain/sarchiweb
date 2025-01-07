import shortuuid
from django.conf import settings
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from .models import Blog


class PostListViewTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # disable any active signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []

        post_id = shortuuid.ShortUUID().random(length=16)
        load_image_1 = f'{settings.PROJECT_DIR}/static/images/logo.png'

        # create model
        cls.blog = baker.make(
            Blog,
            post_id=post_id,
            title='Blockchain Master Class',
            slug='blockchain_master_class',
            featured_image=load_image_1
        )

    def tearDown(self):
        # Clean up run after every test method.
        self.blog.delete()

    def test_blog_list_views(self):
        response = self.client.get(reverse('blog_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.charset, 'utf-8')
        self.assertTrue('blockchain' in str(response.content))
        self.assertTrue('main.css' in str(response.content))
        self.assertFalse('csrfmiddlewaretoken' in str(response.content))

    def test_blog_detail_views(self):
        response = self.client.get(reverse('blog_details', kwargs={'id': self.blog.id, 'slug': self.blog.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.charset, 'utf-8')
        self.assertTrue(self.blog.title in str(response.content))
        self.assertTrue('logo.png' in self.blog.first_section_image.name)
        self.assertTrue('UJ.png' in self.blog.fifth_section_image.name)
