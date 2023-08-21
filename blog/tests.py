from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
import shortuuid
from model_bakery import baker
from .models import Blog


class PostListViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # disable any active signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []

        id = shortuuid.ShortUUID().random(length=16)
        load_image_1 = f'{settings.PROJECT_DIR}/static/images/logo.png'
        load_image_2 = f'{settings.PROJECT_DIR}/static/images/main-logo.png'
        load_image_3 = f'{settings.PROJECT_DIR}/static/images/UJ.png'

        # create model
        cls.bootcamp = baker.make(
            Blog,
            id=id,
            title='Blockchain Master Class',
            slug='blockchain_master_class',
            first_section_image=load_image_1,
            third_section_image=load_image_2,
            fifth_section_image=load_image_3,
        )

    def tearDown(self):
        # Clean up run after every test method.
        self.bootcamp.delete()

    def test_blog_list_views(self):
        response = self.client.get(reverse('blog_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.charset, 'utf-8')
        self.assertTrue('blockchain' in str(response.content))
        self.assertTrue('main.css' in str(response.content))
        self.assertTrue('csrfmiddlewaretoken' in str(response.content))

    def test_blog_detail_views(self):
        response = self.client.get(
            reverse('blog_details', kwargs={'id': self.bootcamp.id, 'slug': self.bootcamp.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.charset, 'utf-8')
        self.assertTrue(self.bootcamp.title in str(response.content))
        self.assertTrue(
            self.bootcamp.first_section_image.name == self.bootcamp.first_section_image.name
        )
        self.assertTrue(
            self.bootcamp.third_section_image.name == self.bootcamp.third_section_image.name
        )
        self.assertTrue('csrfmiddlewaretoken' in str(response.content))
