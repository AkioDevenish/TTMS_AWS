from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Configure for hourly interval with task locking
app.conf.beat_schedule = {
    'fetch-weather-data-hourly': {
        'task': 'database.tasks.fetch_weather_data',
        'schedule': 3600.0,  # 3600 seconds = 1 hour
        'options': {
            'expires': 3600,
            'max_retries': 0
        }
    },
}

# Prevent multiple tasks from running simultaneously
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_ignore_result = True