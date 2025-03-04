from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import logging
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

logger = logging.getLogger(__name__)
logger.info("Registering Celery tasks...")

# Configure beat schedule
app.conf.beat_schedule = {
    'data-fetcher': {
        'task': 'database.tasks.data_fetcher',  # Make sure this matches exactly
        'schedule': crontab(minute=0),  # Run at the start of every hour
        'options': {
            'expires': 3300,
            'max_retries': 2,
            'retry_backoff': True
        }
    },
    'check-station-health': {
        'task': 'database.tasks.check_station_health',
        'schedule': 60.0,
        'options': {
            'expires': 300,
            'max_retries': 2,
            'retry_backoff': True
        }
    }
}

# Load tasks from all registered Django app configs
app.autodiscover_tasks()
logger.info("Tasks registered: %s", app.tasks.keys())

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Configure for 20-second interval with task locking
app.conf.beat_schedule = {
    'data-fetcher': {
        'task': 'database.tasks.data_fetcher',
        'schedule': crontab(minute=0),  # Run at the start of every hour
        'options': {
            'expires': 3300,
            'max_retries': 2,
            'retry_backoff': True,
            'time_limit': 3600,
            'soft_time_limit': 3300
        }
    },

    'deactivate-expired-accounts': {
        'task': 'database.tasks.deactivate_expired_accounts',
        'schedule': 60.0,  # Run every minute instead of every second
        'options': {
            'expires': 55,  # Task expires after 55 seconds
            'max_retries': 0
        }
    },

    'check-station-health': {
        'task': 'database.tasks.check_station_health',
        'schedule': 60.0,
        'options': {
            'expires': 300,
            'max_retries': 2,
            'retry_backoff': True
        }
    }
}

# Task execution settings
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_time_limit = 3600  # 1 hour
app.conf.task_soft_time_limit = 3300  # 55 minutes

# Prevent multiple tasks from running simultaneously
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_ignore_result = True