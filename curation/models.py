from django.db import models

from list.models import List


class FeaturedList(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Featured Lists"
        verbose_name = "Featured List"

    def __str__(self):
        return str(self.list.name)
