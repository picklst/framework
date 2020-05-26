from django.conf import settings
from django.db import models

from list.models import List, Item, Position
from user.models import UserSubscription

User = settings.AUTH_USER_MODEL


class FollowUserRequest(models.Model):
    respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_respondent')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_requester')
    timestamp = models.DateTimeField(auto_now=True)

    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'follow_user_request'
        verbose_name = "Follow User Request"
        verbose_name_plural = "Follow User Requests"

    def __str__(self):
        return str(self.id)


class ListRequest(models.Model):
    respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_request_respondent')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_requester')
    subject = models.CharField(max_length=255, default='', blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True, blank=True, related_name='requested_list')
    
    class Meta:
        db_table = 'list_request'
        verbose_name = "List Request"
        verbose_name_plural = "List Requests"

    def __str__(self):
        return str(self.id)


class ListEntry(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_entry_contributor')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    positionRequested = models.PositiveSmallIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='list_entry_approver')

    class Meta:
        db_table = 'list_entry'
        verbose_name = "List Entry"
        verbose_name_plural = "List Entries"

    def __str__(self):
        return str(self.id)

