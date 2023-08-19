from datetime import datetime
from django.utils.timezone import utc
from django.db.models import signals
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from .models import UserContact
from .forms import UserMessageForm


class ContactTest(TestCase):
    def setUp(self):
        # init current time (timezone aware)
        self.current_timestamp = datetime.now().replace(tzinfo=utc)

    @classmethod
    def setUpTestData(cls):
        # disable signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []

        # create model
        cls.contact_email = baker.make(
            UserContact,
            name='John Deo',
            email='johndeo@ujblockchain.co.za',
            phone='+27111111111',
            message='Hello',
            timestamp=datetime.now().replace(tzinfo=utc),
        )

    def tearDown(self):
        # Clean up run after every test method.
        self.contact_email.delete()

    def test_send_email(self):
        # init model
        model = self.contact_email

        # update model
        model.email = 'hello@ujblockchain.co.za'
        model.save(update_fields=['email'])

        self.assertEqual(model.name, 'John Deo')
        self.assertEqual(model.email, 'hello@ujblockchain.co.za')
        self.assertEqual(model.clean_fields(), None)
        self.assertEqual(model.clean(), None)
        self.assertNotEqual(model.timestamp, self.current_timestamp)
        # check model filed max length
        max_length = UserContact._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)