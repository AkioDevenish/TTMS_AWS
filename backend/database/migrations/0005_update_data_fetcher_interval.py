from django.db import migrations

def update_data_fetcher_interval(apps, schema_editor):
    TaskExecution = apps.get_model('database', 'TaskExecution')
    TaskExecution.objects.filter(task_name='data_fetcher').update(interval=3600)

class Migration(migrations.Migration):
    dependencies = [
        ('database', '0004_taskexecution'),
    ]

    operations = [
        migrations.RunPython(update_data_fetcher_interval),
    ] 