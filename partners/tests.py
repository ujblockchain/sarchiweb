from datetime import datetime
from django.conf import settings
from django.utils.timezone import utc
from django.db.models import signals
from django.test import TestCase
from model_bakery import baker
from .models import Partners


class PartnerTest(TestCase):
    def setUp(self):
        # init current time (timezone aware)
        self.current_timestamp = datetime.now().replace(tzinfo=utc)

    @classmethod
    def setUpTestData(cls):
        # disable signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []

        # init image
        image = f'{settings.BASE_DIR}/media/partners/logo/UJ.png'

        # create model
        cls.partner = baker.make(
            Partners,
            name='UJ',
            image=image,
        )

    def tearDown(self):
        # Clean up run after every test method.
        self.partner.delete()

    def test_partner(self):
        # init model
        model = self.partner

        self.assertEqual(model.name, 'UJ')
        self.assertTrue('UJ' in model.image.name)
        self.assertEqual(model.clean_fields(), None)
        self.assertEqual(model.clean(), None)
        self.assertNotEqual(model.timestamp, self.current_timestamp)
        # check model filed max length
        max_length = Partners._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)
