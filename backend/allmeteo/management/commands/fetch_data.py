import requests
from django.core.management.base import BaseCommand
from allmeteo.models import WeatherMeasurement
import time
from django.utils import timezone
from dateutil import parser
from datetime import datetime, timezone as dt_timezone
from datetime import timedelta
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

        # Time range configuration for December 1st to December 2nd, 2024
        current_date_start = datetime(2024, 12, 1).date()
        current_date_end = datetime(2024, 12, 2).date()

        # Define the time range from 9 AM on December 1st to 10 AM on December 2nd
        START_DATE = datetime.combine(current_date_start, datetime.min.time()) + timedelta(hours=9)
        END_DATE = datetime.combine(current_date_end, datetime.min.time()) + timedelta(hours=10)

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
        """Fetch data from the API with retry logic."""
        for attempt in range(max_retries):
            try:
                response = requests.get(base_url, headers=headers, params=params)
                if response.status_code == 200:
                    logger.info("Successfully fetched data from the API.")
                    logger.debug(f"API response: {response.text}")
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
        """Process and save measurements to the database."""
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
                    sensor_sn = "Unknown"

                # Process and save each reading
                for reading in readings:
                    datetime_str = reading.get("datetime")
                    timestamp = self.parse_datetime(datetime_str)

                    # Only process the reading if the datetime is valid and value exists
                    if timestamp and reading.get("value") is not None:
                        # Create a new WeatherMeasurement for each reading
                        measurement = WeatherMeasurement(
                            device_name=metadata.get("device_name"),
                            sensor_name=metadata.get("sensor_name"),
                            sensor_sn=sensor_sn,
                            units=metadata.get("units"),
                            value=reading["value"],  # Explicitly set the value
                            timestamp=timestamp,
                            timestamp_utc=self.parse_datetime(reading.get("timestamp_utc")) or timezone.now(),
                            precision=reading.get("precision"),
                            error_flag=reading.get("error_flag", False),
                            error_description=reading.get("error_description", "")
                        )
                        measurement.save()
                        logger.info(f"Saved measurement for sensor {measurement.sensor_name} at {timestamp}")

    def parse_datetime(self, datetime_str):
        """Parse the datetime string from the API and make it timezone-aware."""
        if isinstance(datetime_str, str):
            try:
                logger.debug(f"Parsing datetime string: {datetime_str}")
                parsed_datetime = parser.parse(datetime_str)

                if parsed_datetime.tzinfo is None:
                    parsed_datetime = timezone.make_aware(parsed_datetime, dt_timezone.utc)

                return parsed_datetime
            except ValueError:
                logger.warning(f"Invalid datetime format: {datetime_str}")
                return None
        
        elif isinstance(datetime_str, (int, float)):
            try:
                if datetime_str < 0 or datetime_str > 32503680000:  # Up to year 3000
                    logger.warning(f"Invalid Unix timestamp value: {datetime_str}. Skipping.")
                    return None
                timestamp = datetime.utcfromtimestamp(datetime_str)
                return timezone.make_aware(timestamp, dt_timezone.utc)
            except (ValueError, OSError) as e:
                logger.warning(f"Invalid Unix timestamp value: {datetime_str} ({e}). Skipping.")
                return None
        else:
            logger.warning(f"Invalid datetime value: {datetime_str}")
            return None