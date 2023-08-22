from datetime import datetime
from django.utils.timezone import utc
from django.db.models import signals
from django.test import TestCase
from decouple import config
from model_bakery import baker
import shortuuid
from .models import Projects


class ProjectTest(TestCase):
    def setUp(self):
        # init current time (timezone aware)
        self.current_timestamp = datetime.now().replace(tzinfo=utc)

    @classmethod
    def setUpTestData(cls):
        # disable signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []
        
        #generate id
        id = shortuuid.ShortUUID().random(length=16)

        # create model
        cls.partner = baker.make(
            Projects,
            id=id,
            title='FoodTrolley',
            project_progress = 40,
            project_commit_count = 100, 
            distribution_count= 2000,
            total_distribution_count=3000,
            lines_of_code= 2000,
            coding_hours=93,
        )

    def tearDown(self):
        # Clean up run after every test method.
        self.partner.delete()

    def test_projects(self):
        # init model
        model = self.partner

        self.assertEqual(model.title, 'FoodTrolley')
        self.assertTrue(self.id in model.id)
        self.assertEqual(model.clean_fields(), None)
        self.assertEqual(model.clean(), None)
        self.assertNotEqual(model.timestamp, self.current_timestamp)
        # check model filed max length
        commit_count = Projects._meta.get_field('title').max_length
        self.assertEqual(commit_count, 200)
