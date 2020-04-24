from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from graphql_jwt.refresh_token.models import RefreshToken
from graphql_jwt.signals import token_issued

from framework.utils.cornflakes.decorators import model_config
from framework.utils.cornflakes.fields import ShadedIDField
from media.fields import MediaField
from media.storages import UserAvatarStorage, UserCoverStorage


@model_config()
class User(AbstractUser):
    id = ShadedIDField(primary_key=True, null=False)
    # email to communicate with the user
    email = models.EmailField(unique=True, null=False, blank=False)

    # boolean, whether the account belongs to a verified celebrity/personality/organization
    isVerified = models.BooleanField(default=False)
    # boolean, whether the profile of this user should be viewable only by his followers
    # if set to true, users would have to send follow requests to become followers
    isProfilePrivate = models.BooleanField(default=False)
    # boolean, whether the account belongs to a business entity and should business features be enabled
    isBusinessProfile = models.BooleanField(default=False)

    # varchar(255), stores user's first name
    first_name = models.CharField(max_length=255, default='', blank=True, verbose_name='First Name')
    # varchar(255), stores user's last name
    last_name = models.CharField(max_length=255, default='', blank=True, verbose_name='Last Name')
    # varchar(255), a short self-written bio of the user that will be shown in users' profile
    bio = models.CharField(max_length=255, default='', blank=True, verbose_name='Bio')
    # varchar(255) with url validation, this url selected by the user will be shown in user's profile
    url = models.URLField(max_length=255, default='', blank=True, verbose_name='URL')

    # file field with image/size validation, the user's avatar
    # will be publicly visible (even if user has set 'isProfilePrivate')
    avatar = MediaField(
        storage=UserAvatarStorage(),
        max_size=1024 * 1024 * 5,
        content_types=[
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
        ],
        null=True, blank=True
    )
    # file field with image/size validation, a cover image for the user's profile
    # will be publicly visible (even if user has set 'isProfilePrivate')
    cover = MediaField(
        storage=UserCoverStorage(),
        max_size=1024 * 1024 * 8,
        content_types=[
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
        ],
        null=True, blank=True
    )


# user login function that stores last login timestamp when a user login
def handle_user_login(sender, user, request, **kwargs):
    user.last_login = timezone.now()
    user.save()


# token_issued signal is connected with the login handler function
token_issued.connect(handle_user_login)


# deletes the user's avatar and cove image from storage if the user is deleted
@receiver(post_delete, sender=User)
def submission_delete(sender, instance, **kwargs):
    instance.cover.delete(save=False)
    instance.avatar.delete(save=False)


@model_config()
class UserSubscription(models.Model):
    id = ShadedIDField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='user')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Subscriber', related_name='follower')
    createdTimestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_subscription'
        unique_together = [['user', 'subscriber']]
        verbose_name = "User Subscription"
        verbose_name_plural = "User Subscriptions"

    def __str__(self):
        return str(self.id)


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refreshToken = models.OneToOneField(RefreshToken, on_delete=models.CASCADE)
    lastSeenTimestamp = models.DateTimeField(auto_now=True)
    ipAddress = models.GenericIPAddressField(null=True, blank=True)
    operatingSystem = models.CharField(max_length=63, null=False, blank=True, default='')
    browser = models.CharField(max_length=63, null=False, blank=True, default='')
    device = models.CharField(max_length=63, null=False, blank=True, default='')

    class Meta:
        db_table = 'user_session'
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        return str(self.id)


__all__ = [
    'User',
    'UserSubscription',
    'UserSession'
]
