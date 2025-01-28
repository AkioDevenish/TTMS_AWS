from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .tasks import deactivate_expired_accounts
from datetime import datetime, timedelta

def start():
    scheduler = BackgroundScheduler()
    
    # Run the deactivation check every day at midnight
    scheduler.add_job(
        deactivate_expired_accounts,
        'cron',
        hour=0,
        minute=0,
        id='deactivate_expired_accounts'
    )
    
    scheduler.start() 