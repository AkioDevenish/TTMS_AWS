# Generated by Django 5.0.1 on 2025-02-26 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='receipt_verified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
