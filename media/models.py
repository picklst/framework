from django.db import models
from django.conf import settings

from framework.utils.cornflakes.decorators import model_config
from framework.utils.cornflakes.fields import ShadedIDField
from media.fields import MediaField
from media.storages import UserMediaStorage

User = settings.AUTH_USER_MODEL


@model_config()
class Media(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    id = ShadedIDField(primary_key=True, null=False)
    # boolean, whether the media contains material
    isSensitive = models.BooleanField(default=False)
    # boolean, whether the media contains explicit material
    isExplicit = models.BooleanField(default=False)
    # boolean, whether the media is taken down due to violations
    isTakenDown = models.BooleanField(default=False)

    # foreign key to the user who uploaded this media
    uploader = models.ForeignKey(User, verbose_name='Uploader', on_delete=models.CASCADE)
    # timestamp of upload
    timestamp = models.DateTimeField(auto_now=True)

    # type of media
    type = models.CharField(max_length=15, default='image')

    # aspect ratio of media
    aspect = models.DecimalField(decimal_places=2, max_digits=3, default=1)

    # the file, actual media asset
    asset = MediaField(
        storage=UserMediaStorage(),
        max_size=1024,
        content_types=[
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
            'video/ogg', 'video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-ms-wmv', 'video/webm',
            'audio/aac', 'audio/mpeg', 'audio/mp3'
        ]
    )

    class Meta:
        db_table = 'media'
        verbose_name_plural = "Media"
        verbose_name = "Media"

    def __str__(self):
        return str(self.id)


# # deletes the media from storage if Media object is deleted
# @receiver(post_delete, sender=Media)
# def submission_delete(sender, instance, **kwargs):
#     instance.asset.delete(save=False)


__all__ = [
    'Media',
]
