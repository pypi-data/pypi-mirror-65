# Generated by Django 2.2 on 2020-03-23 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0041_slugs'),
    ]

    operations = [
        migrations.AddField(
            model_name='cameramodel',
            name='mirror_lockup',
            field=models.BooleanField(blank=True, help_text='Whether the camera has mirror lock-up', null=True, verbose_name='Mirror lock-up'),
        ),
    ]
