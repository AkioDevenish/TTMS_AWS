from celery import shared_task
from django.core.management import call_command
from celery.utils.log import get_task_logger
from celery import Task
from .models import Station, StationHealthLog, Measurement, TaskExecution
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from .models import User
import logging
from django.contrib.auth import get_user_model
from django.db import transaction
from celery.exceptions import SoftTimeLimitExceeded
from io import StringIO

logger = logging.getLogger(__name__)

User = get_user_model()

class SingletonTask(Task):
    _is_running = False

    def __call__(self, *args, **kwargs):
        if self._is_running:
            logger.info('Task is already running')
            return None
        self._is_running = True
        try:
            return super().__call__(*args, **kwargs)
        finally:
            self._is_running = False

@shared_task(bind=True, base=SingletonTask, soft_time_limit=3300, time_limit=3600)
def data_fetcher(self):
    logger.info("Starting data_fetcher task")
    try:
        now = timezone.now()
        # Round to previous hour for last_run
        last_run = now.replace(minute=0, second=0, microsecond=0)
        
        # Create initial record with aligned timing
        task_record = TaskExecution.objects.get_or_create(
            task_name='data_fetcher',
            defaults={
                'status': 'running',
                'interval': 3600,
                'last_run': last_run
            }
        )[0]
        
        task_record.status = 'running'
        task_record.last_run = last_run  # Ensure last_run is set correctly
        task_record.save()
        
        try:
            logger.info("Calling data_fetcher management command")
            output = StringIO()
            # Call the management command directly
            call_command('data_fetcher', stdout=output)
            output_text = output.getvalue()
            logger.info(f"Command output: {output_text}")
            
            # Update success status
            TaskExecution.objects.filter(task_name='data_fetcher').update(
                status='success',
                last_run=last_run,
                interval=3600
            )
            return "Data fetcher completed successfully"
            
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            TaskExecution.objects.filter(task_name='data_fetcher').update(
                status='failed',
                last_run=last_run,
                interval=3600
            )
            return f"Data fetcher failed: {str(e)}"
            
    except SoftTimeLimitExceeded:
        logger.warning("Task approaching timeout - gracefully stopping")
        TaskExecution.objects.filter(task_name='data_fetcher').update(
            status='timeout',
            last_run=last_run,
            interval=3600
        )
        return "Task timed out gracefully"

@shared_task(bind=True, base=SingletonTask, soft_time_limit=240, time_limit=300)
def check_station_health(self):
    try:
        logger.info("Starting check_station_health task")
        
        # Create task execution record first
        task_record, created = TaskExecution.objects.get_or_create(
            task_name='check_station_health',
            defaults={
                'status': 'running',
                'interval': 60
            }
        )
        
        if not created:
            task_record.status = 'running'
            task_record.save()
            
        logger.info("Task execution record created/updated")
        
        try:
            stations = Station.objects.all()
            now = timezone.now()
            one_hour_ago = now - timedelta(hours=1)
            
            for station in stations:
                # Get latest health log for this station
                latest_health = StationHealthLog.objects.filter(
                    station=station,
                    created_at__gte=one_hour_ago
                ).order_by('-created_at').first()
                
                # Determine activity status based on health log
                if latest_health:
                    # For 3D_Paws stations, check CSS status
                    if station.brand.name == "3D_Paws":
                        is_active = latest_health.connectivity_status in ["Excellent", "Good", "Fair"]
                    # For other stations, check if we have recent health data
                    else:
                        is_active = True
                else:
                    is_active = False
                
                # Update station status in database
                station.is_active = is_active
                station.last_checked = now
                station.save()

                # Create new health log entry if none exists for current period
                if not latest_health:
                    StationHealthLog.objects.create(
                        station=station,
                        battery_status="Unknown",
                        connectivity_status="No Data",
                        created_at=now
                    )
            
            # Update success status
            TaskExecution.objects.filter(task_name='check_station_health').update(
                status='success',
                last_run=timezone.now()
            )
            return "Station health check completed successfully"
            
        except SoftTimeLimitExceeded:
            logger.warning("Task approaching timeout - gracefully stopping")
            TaskExecution.objects.filter(task_name='check_station_health').update(
                status='timeout',
                last_run=timezone.now()
            )
            return "Task timed out gracefully"
            
    except Exception as e:
        logger.error(f"Station health check failed: {str(e)}")
        TaskExecution.objects.filter(task_name='check_station_health').update(
            status='failed',
            last_run=timezone.now()
        )
        raise e

@shared_task(
    base=SingletonTask,
    bind=True,
    max_retries=0,
    time_limit=300,
    soft_time_limit=270
)
def deactivate_expired_accounts(self):
    try:
        now = timezone.now()
        logger.info(f"Starting account expiration check at {now}")
        
        # Using transaction.atomic() for database consistency
        with transaction.atomic():
            expired_users = User.objects.select_for_update().filter(
                status='Active',
                expires_at__isnull=False,
                expires_at__lt=now  # Changed to lt to be more precise
            )
            
            count = expired_users.count()
            if count > 0:
                # Debug log each user's expiration status
                for user in expired_users:
                    logger.info(f"Checking user: {user.email}")
                    logger.info(f"Expiration time: {user.expires_at}")
                    logger.info(f"Current time: {now}")
                
                # Bulk update
                expired_users.update(
                    status='Inactive',
                    updated_at=now
                )
                logger.info(f"Deactivated {count} expired user accounts")
            else:
                logger.info(f"No expired accounts found at {now}")
            return count
            
    except Exception as e:
        logger.error(f"Error in deactivate_expired_accounts: {str(e)}")
        logger.exception(e)
        raise