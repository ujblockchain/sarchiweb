import uuid

from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from .models import Contact


class ContactModelTest(TestCase):
    def setUp(self):
        full_uuid = str(uuid.uuid4()).replace('-', '')
        self.expected_id = full_uuid[:16]
        self.contact = baker.make(
            Contact,
            id=self.expected_id,
            first_name='John',
            last_name='Doe',
            email='test@ujblockchain.co.za',
            message='Hello, there!!!',
        )

        self.contact_url = reverse('home')

    def tearDown(self):
        self.contact.delete()

    def test_id_field(self):
        self.assertEqual(len(self.contact.id), 16)
        self.assertTrue(self.contact.id.isalnum())

        new_full_uuid = str(uuid.uuid4()).replace('-', '')
        new_expected_id = new_full_uuid[:16]
        self.assertNotEqual(self.contact.id, new_expected_id)

    def test_message_creation(self):
        self.assertEqual(self.contact.first_name, 'John')
        self.assertEqual(self.contact.email, 'test@ujblockchain.co.za')
        self.assertEqual(self.contact.message, 'Hello, there!!!')
        self.assertIsNotNone(self.contact.date_received)

    def test_testimony_details(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact')
        self.assertTemplateUsed(response, 'pages/index.html')
