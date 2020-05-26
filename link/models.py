from django.db import models

from framework.utils.cornflakes.fields import ShadedIDField


class Link(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    id = ShadedIDField(primary_key=True, null=False)

    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, default='', blank=True)
    description = models.CharField(max_length=511, default='', blank=True)
    image = models.CharField(max_length=255, default='', blank=True)
    retrievedTimestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Links"
        verbose_name = "Link"

    def __str__(self):
        return str(self.url)
