from django.db import models
from django.conf import settings

from list.models import List, Item

User = settings.AUTH_USER_MODEL


class ChangeLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ListChangeLog(ChangeLog):
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    class Meta:
        db_table = 'changelog_list'
        verbose_name_plural = "List Changelog"
        verbose_name = "List Changelog"

    def __str__(self):
        return self.id


class ItemChangeLog(ChangeLog):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = 'changelog_item'
        verbose_name_plural = "Item Changelog"
        verbose_name = "Item Changelog"

    def __str__(self):
        return self.id
