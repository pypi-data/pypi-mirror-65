# Generated by Django 2.2.9 on 2020-03-05 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0025_convert_shoe_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cameramodel',
            name='coldshoe',
        ),
        migrations.RemoveField(
            model_name='cameramodel',
            name='hotshoe',
        ),
    ]
