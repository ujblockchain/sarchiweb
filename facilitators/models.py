from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from blog.validate_image import clean_image


class Facilitators(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
        primary_key=True,
    )
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='facilitator')
    image = models.ImageField(upload_to='facilitators/image/', validators=[clean_image])
    phone_number = models.CharField(max_length=100)
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['date_created']
        verbose_name = "Facilitator"
        verbose_name_plural = "Facilitators"
