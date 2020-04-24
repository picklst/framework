from django.db import models

from framework.utils.cornflakes.decorators import model_config
from framework.utils.cornflakes.fields import ShadedIDField


@model_config()
class Topic(models.Model):
    id = ShadedIDField(primary_key=True, null=False)
    # varchar(63), uniquely identified field for a topic
    slug = models.SlugField(max_length=63, unique=True, verbose_name='Slug')
    # varchar(63), name for the topic
    name = models.CharField(max_length=63, verbose_name='Name')
    # varchar(63), plural name for the topic
    namePlural = models.CharField(max_length=63, verbose_name='Name (Plural)')

    class Meta:
        db_table = 'topic'
        verbose_name_plural = "Topics"
        verbose_name = "Topic"

    def __str__(self):
        return str(self.name)


@model_config()
class Tag(models.Model):
    # unsigned INT64, auto incremented, primary Key
    # always kept secret
    id = ShadedIDField(primary_key=True, null=False)
    # varchar(63), uniquely identified field for a tag
    name = models.SlugField(max_length=63, unique=True, verbose_name='Tag Name')

    class Meta:
        db_table = 'tag'
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return str(self.name)
