from django.db.models import signals
from django.test import TestCase
from django.urls import reverse


class PagesViewTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # disable any active signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []

    def test_home_page_views(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.charset, 'utf-8')
        self.assertTrue('Blockchain' in str(response.content))
        self.assertTrue('main.js' in str(response.content))
        self.assertTrue('csrfmiddlewaretoken' in str(response.content))
