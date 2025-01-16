from celery import shared_task
from django.core.management import call_command
from celery.utils.log import get_task_logger
from celery import Task
from .models import Station, StationHealthLog
from django.utils import timezone

logger = get_task_logger(__name__)

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

@shared_task(
    base=SingletonTask,
    bind=True,
    max_retries=0,
    time_limit=3000,
    soft_time_limit=2700
)
def fetch_weather_data(self):
    try:
        logger.info("Starting weather data fetch")
        call_command('data_fetcher')
        logger.info("Completed weather data fetch")
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise

@shared_task
def check_station_health():
    stations = Station.objects.all()
    for station in stations:
        StationHealthLog.objects.create(
            station=station,
            battery_status='CHECK',
            connectivity_status='CHECK',
        )