import requests
from django.core.management.base import BaseCommand
from allmeteo.models import WeatherMeasurement, WeatherReading
import time
from django.utils import timezone
from dateutil import parser
from datetime import datetime, timezone as dt_timezone
from datetime import datetime, timedelta
import logging



# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetch data from Zentra API and save it to the database."

    def handle(self, *args, **kwargs):
        # API Configuration
        BASE_URL = "https://zentracloud.com/api/v4/get_readings/"
        API_TOKEN = "3db9d133d878433b0c7f4a26adfa566426921e0e"
        DEVICE_SN = "z6-26732"

        # Headers for API request
        headers = {"Authorization": f"Token {API_TOKEN}"}

        # Time range (adjust these as needed)
        current_date = datetime.now().date()
        START_DATE = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=9)  # 9 AM today
        END_DATE = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=10)  # 10 AM today

        params = {
            "device_sn": DEVICE_SN,
            "start_date": START_DATE.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": END_DATE.strftime("%Y-%m-%d %H:%M:%S"),
            "output_format": "json",
            "per_page": 30,
            "page_num": 1,
            "sort_by": "desc"
        }

        # Fetch the data from the API
        response = self.fetch_data(BASE_URL, headers, params)

        if response:
            self.process_measurements(response)
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch data."))

    def fetch_data(self, base_url, headers, params, max_retries=5, initial_delay=60):
        """Function to fetch data from the API with retry logic."""
        for attempt in range(max_retries):
            try:
                response = requests.get(base_url, headers=headers, params=params)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    logger.error("Authentication failed. Please check your API token.")
                    return None
                elif response.status_code == 403:
                    logger.error("Forbidden. You might not have permission to access this resource.")
                    return None
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', initial_delay))
                    logger.warning(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    logger.error(f"Unexpected status code: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                logger.error(f"An error occurred: {e}")
                return None
        logger.error(f"Max retries ({max_retries}) reached. Unable to fetch data.")
        return None

    def process_measurements(self, data):
        """Function to process and save measurements to the database."""
        if 'data' not in data:
            self.stdout.write(self.style.ERROR("No 'data' key found in the API response."))
            return

        # Iterate through each measurement in the response
        for measurement_name, measurement_data in data['data'].items():
            for config in measurement_data:
                metadata = config.get("metadata", {})
                readings = config.get("readings", [])

                # Check if 'sensor_sn' is missing, and provide a default value if necessary
                sensor_sn = metadata.get("sensor_sn")
                if not sensor_sn:
                    logger.warning(f"Missing 'sensor_sn' for {metadata.get('device_name')} - {metadata.get('sensor_name')}. Using 'Unknown'.")
                    sensor_sn = "Unknown"  # Or any default value you prefer

                # Create or get the WeatherMeasurement object
                measurement, created = WeatherMeasurement.objects.get_or_create(
                    device_name=metadata.get("device_name"),
                    sensor_name=metadata.get("sensor_name"),
                    sensor_sn=sensor_sn,
                    units=metadata.get("units"),
                )

                # Process and save each reading
                for reading in readings:
                    # Get the datetime string and safely parse it
                    datetime_str = reading.get("datetime")
                    timestamp = self.parse_datetime(datetime_str)

                    # Only save the reading if the datetime is valid
                    if timestamp:
                        self.save_weather_reading(measurement, reading, timestamp)

    def parse_datetime(self, datetime_str):
        """Parse the datetime string from the API and make it timezone-aware."""
        if isinstance(datetime_str, str):
            try:
                logger.debug(f"Parsing datetime string: {datetime_str}")
                # Use dateutil.parser.parse to handle various datetime formats including timezone
                parsed_datetime = parser.parse(datetime_str)

                # Make the parsed datetime timezone-aware if it's naive
                if parsed_datetime.tzinfo is None:
                    # If datetime is naive, make it aware in UTC
                    parsed_datetime = timezone.make_aware(parsed_datetime, dt_timezone.utc)

                return parsed_datetime
            except ValueError:
                logger.warning(f"Invalid datetime format: {datetime_str}")
                return None
        
        elif isinstance(datetime_str, (int, float)):
            try:
                # Validate Unix timestamp range (seconds since the Unix epoch)
                if datetime_str < 0 or datetime_str > 32503680000:  # Up to year 3000
                    logger.warning(f"Invalid Unix timestamp value: {datetime_str}. Skipping.")
                    return None
                # Convert Unix timestamp to datetime
                timestamp = datetime.utcfromtimestamp(datetime_str)
                return timezone.make_aware(timestamp, dt_timezone.utc)
            except (ValueError, OSError) as e:
                logger.warning(f"Invalid Unix timestamp value: {datetime_str} ({e}). Skipping.")
                return None
        else:
            logger.warning(f"Invalid datetime value: {datetime_str}")
            return None
    
    def save_weather_reading(self, measurement, reading, timestamp):
        """Create a WeatherReading entry and save it."""
        timestamp_utc = self.parse_datetime(reading.get("timestamp_utc"))
        
        # If timestamp_utc is None, set it to the current UTC time
        if not timestamp_utc:
            timestamp_utc = timezone.now()  # Use current UTC time as fallback
        
        # Ensure timestamp_utc is timezone-aware
        if timezone.is_naive(timestamp_utc):
            timestamp_utc = timezone.make_aware(timestamp_utc, timezone.utc)

        WeatherReading.objects.create(
            measurement=measurement,
            value=reading["value"],
            datetime=timestamp,
            timestamp_utc=timestamp_utc,
            precision=reading.get("precision"),
            error_flag=reading.get("error_flag", False),
            error_description=reading.get("error_description", ""),
        )
        logger.info(f"Saved reading for sensor {measurement.sensor_name} at {timestamp}")
