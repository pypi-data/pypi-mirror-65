# Generated by Django 2.2.4 on 2019-11-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0016_auto_20191107_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cameramodel',
            name='metering_type',
            field=models.CharField(blank=True, choices=[('Cadmium sulphide CdS', 'Cadmium sulphide CdS'), ('Selenium', 'Selenium'), ('Silicon', 'Silicon')], help_text='Metering type used on this camera model', max_length=25, null=True),
        ),
        migrations.DeleteModel(
            name='MeteringType',
        ),
    ]
