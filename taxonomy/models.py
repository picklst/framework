from django.db import models


class Topic(models.Model):
    # varchar(63), uniquely identified field for a topic
    slug = models.SlugField(max_length=63, unique=True, verbose_name='Slug')
    # varchar(63), name for the topic
    name = models.CharField(max_length=63, verbose_name='Name')
    # varchar(63), plural name for the topic
    namePlural = models.CharField(max_length=63, verbose_name='Name (Plural)')

    class Meta:
        verbose_name_plural = "Topics"
        verbose_name = "Topic"

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    # unsigned INT64, auto incremented, primary Key
    # always kept secret
    id = models.BigAutoField(primary_key=True)
    # varchar(63), uniquely identified field for a tag
    name = models.SlugField(max_length=63, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name_plural = "HashTags"
        verbose_name = "HashTag"

    def __str__(self):
        return str(self.name)
