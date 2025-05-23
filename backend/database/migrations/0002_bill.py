# Generated by Django 5.0.1 on 2025-02-26 21:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_num', models.CharField(max_length=255, unique=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('package', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receipt_num', models.CharField(blank=True, max_length=255, null=True)),
                ('receipt_upload', models.FileField(blank=True, null=True, upload_to='receipts/%Y/%m/%d/')),
                ('receipt_createat', models.DateTimeField(blank=True, null=True)),
                ('receipt_verified', models.BooleanField(default=False)),
                ('receipt_verifiedby', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_bills', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bills',
            },
        ),
    ]
