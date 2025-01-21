from celery import shared_task
from django.core.management import call_command
from celery.utils.log import get_task_logger
from celery import Task
from .models import Station, StationHealthLog, Measurement
from django.utils import timezone
from datetime import datetime

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
    now = timezone.now()
    
    for station in stations:
        # Get latest measurement for this station
        latest_measurement = Measurement.objects.filter(
            station=station
        ).order_by('-date', '-time').first()
        
        # Determine connectivity status
        if latest_measurement:
            measurement_datetime = datetime.combine(
                latest_measurement.date, 
                latest_measurement.time
            ).replace(tzinfo=timezone.utc)
            
            # If last measurement is within last hour, consider connected
            time_difference = now - measurement_datetime
            if time_difference.total_seconds() <= 3600:  # 1 hour
                connectivity_status = "Connected"
            else:
                connectivity_status = "Disconnected"
        else:
            connectivity_status = "No Data"

        # Get battery related measurements
        battery_measurements = Measurement.objects.filter(
            station=station,
            sensor__type__in=['battery', 'bpc', 'css', 'Battery Percent', 'Battery Voltage'],
            date=now.date()
        ).order_by('-time').first()

        battery_status = (
            f"{battery_measurements.value}%" if battery_measurements 
            else "Unknown"
        )

        StationHealthLog.objects.create(
            station=station,
            battery_status=battery_status,
            connectivity_status=connectivity_status,
        )