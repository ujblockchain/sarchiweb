from django.test import TestCase

# Create your tests here.
from datetime import datetime
from django.utils.timezone import utc
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from .models import BootcampFirst
from .forms import BootcampForm


class BootcampTest(TestCase):
    def setUp(self):
        # init current time (timezone aware)
        self.current_timestamp = datetime.now().replace(tzinfo=utc)

    @classmethod
    def setUpTestData(cls):
        # disable signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []

        # create model
        cls.bootcamp = baker.make(
            BootcampFirst,
            first_name='John',
            last_name='Doe',
            email='johndoe@test.com',
            faculty='FEBE',
            department='Electrical Engineering',
            level='Post Graduate',
            expectation='To build great DApps',
        )

    def tearDown(self):
        # Clean up run after every test method.
        self.bootcamp.delete()

    def test_bootcamp_model(self):
        # init model
        model = self.bootcamp

        # update model
        model.email = 'hello@blockchain.co.za'
        model.save(update_fields=['email'])

        self.assertEqual(model.first_name, 'John')
        self.assertEqual(model.email, 'hello@blockchain.co.za')
        self.assertEqual(model.clean_fields(), None)
        self.assertEqual(model.clean(), None)
        self.assertNotEqual(model.timestamp, self.current_timestamp)
        # check model filed max length
        max_length = BootcampFirst._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)
