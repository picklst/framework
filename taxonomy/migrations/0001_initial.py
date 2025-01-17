# Generated by Django 3.0.4 on 2020-05-26 22:44

from django.db import migrations, models
import framework.utils.cornflakes.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', framework.utils.cornflakes.fields.ShadedIDField(primary_key=True, serialize=False)),
                ('name', models.SlugField(max_length=63, unique=True, verbose_name='Tag Name')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', framework.utils.cornflakes.fields.ShadedIDField(primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=63, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=63, verbose_name='Name')),
                ('namePlural', models.CharField(max_length=63, verbose_name='Name (Plural)')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'db_table': 'topic',
            },
        ),
    ]
