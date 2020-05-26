from django.db import models

from framework.utils.cornflakes.decorators import model_config
from framework.utils.cornflakes.fields import ShadedIDField

from media.models import Media
from user.models import User


@model_config()
class PollOption(models.Model):
    id = ShadedIDField(primary_key=True, null=False)
    name = models.CharField(max_length=255)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'poll_option'
        verbose_name = "Poll Option"
        verbose_name_plural = "Poll Options"

    def __str__(self):
        return str(self.id)


@model_config()
class UserPollChoice(models.Model):
    id = ShadedIDField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('list.Item', on_delete=models.CASCADE)
    choice = models.ForeignKey(PollOption, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'item']]
        db_table = 'user_poll_choice'
        verbose_name = "User Poll Choice"
        verbose_name_plural = "User Poll Choices"

    def __str__(self):
        return str(self.id)
