# Generated by Django 5.1.3 on 2025-01-07 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_alter_measurement_sensor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]
