# Generated by Django 3.0.4 on 2020-05-26 22:44

from django.db import migrations, models
import framework.utils.cornflakes.fields
import media.fields
import media.storages


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', framework.utils.cornflakes.fields.ShadedIDField(primary_key=True, serialize=False)),
                ('isSensitive', models.BooleanField(default=False)),
                ('isExplicit', models.BooleanField(default=False)),
                ('isTakenDown', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(default='image', max_length=15)),
                ('aspect', models.DecimalField(decimal_places=2, default=1, max_digits=3)),
                ('asset', media.fields.MediaField(storage=media.storages.UserMediaStorage(), upload_to='')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Media',
                'db_table': 'media',
            },
        ),
    ]
