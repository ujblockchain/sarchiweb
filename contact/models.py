import uuid

import pgcrypto
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


def generate_custom_id():
    full_uuid = str(uuid.uuid4()).replace('-', '')
    custom_id = full_uuid[:16]
    return custom_id


class Contact(models.Model):
    id = models.CharField(
        default=generate_custom_id,
        editable=False,
        unique=True,
        max_length=20,
        primary_key=True,
    )
    first_name = pgcrypto.EncryptedCharField(max_length=100,
                                             null=False,
                                             blank=False)
    last_name = pgcrypto.EncryptedCharField(max_length=100,
                                            null=False,
                                            blank=False)
    email = pgcrypto.EncryptedEmailField(max_length=254,
                                         null=False,
                                         blank=False)
    message = pgcrypto.EncryptedTextField(max_length=500,
                                          null=False,
                                          blank=False)
    history = HistoricalRecords()
    date_received = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-date_received']
