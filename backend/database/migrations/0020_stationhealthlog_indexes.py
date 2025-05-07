from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='stationhealthlog',
            index=models.Index(fields=['station', '-created_at'], name='station_hea_station_9c13dd_idx'),
        ),
        migrations.AddIndex(
            model_name='stationhealthlog',
            index=models.Index(fields=['created_at'], name='station_hea_created_18b9ca_idx'),
        ),
        migrations.AddIndex(
            model_name='stationhealthlog',
            index=models.Index(fields=['connectivity_status'], name='station_hea_connect_f4d884_idx'),
        ),
    ] 