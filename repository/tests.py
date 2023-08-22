from datetime import datetime
from django.utils.timezone import utc
from django.db.models import signals
from django.test import TestCase
from decouple import config
from model_bakery import baker
from .models import RepoInfo


class RepoTest(TestCase):
    def setUp(self):
        # init current time (timezone aware)
        self.current_timestamp = datetime.now().replace(tzinfo=utc)

    @classmethod
    def setUpTestData(cls):
        # disable signals
        signals.post_save.receivers = []
        signals.pre_save.receivers = []

        # create model
        cls.partner = baker.make(
            RepoInfo,
            active_repo=config('GITHUB_EVENT_URL'),
            total_commit=200,
        )

    def tearDown(self):
        # Clean up run after every test method.
        self.partner.delete()

    def test_repo(self):
        # init model
        model = self.partner

        self.assertEqual(model.active_repo, config('GITHUB_EVENT_URL'))
        self.assertTrue('github' in model.active_repo)
        self.assertEqual(model.clean_fields(), None)
        self.assertEqual(model.clean(), None)
        self.assertNotEqual(model.timestamp, self.current_timestamp)
        # check model filed max length
        commit_count = RepoInfo._meta.get_field('total_commit').default
        self.assertEqual(commit_count, 100)
