from django.db import models
from django.utils import timezone
from blog.validate_image import clean_image


class Partners(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='partners/logo/', validators=[clean_image])
    publish = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_created']
        verbose_name = "Partner"
        verbose_name_plural = "Partners"
