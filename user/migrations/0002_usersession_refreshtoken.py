# Generated by Django 3.0.4 on 2020-05-26 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refresh_token', '0002_auto_20190130_0900'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='refreshToken',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='refresh_token.RefreshToken'),
            preserve_default=False,
        ),
    ]
