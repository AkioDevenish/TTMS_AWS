import requests
from django.core.management.base import BaseCommand
from database.models import Measurement, Station, Sensor, Brand
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from dateutil import parser
import logging
import time
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches data from PAWS, Zentra, and Barani instruments and stores it in the database'

    def handle(self, *args, **kwargs):
        self.fetch_paws_data()
        self.fetch_zentra_data()
        self.fetch_barani_data()
        self.stdout.write(self.style.SUCCESS('Data fetching completed successfully'))

    def fetch_paws_data(self):
        """Fetch data from PAWS instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting PAWS Data Fetch ==='))

        portal_url = "http://3d-trinidad.icdp.ucar.edu"
        user_email = "jerome.ramirez@metoffice.gov.tt"
        api_key = "sVALwcRMyQmjtwYpDPW-"
        start_datetime = "2024-12-04 0:00:00"
        end_datetime = "2024-12-04 23:59:59"

        start = parse_datetime(start_datetime).isoformat() + "Z"
        end = parse_datetime(end_datetime).isoformat() + "Z"

        # Fetch station IDs for the stations with brand_name "3D Paws"
        station_response = requests.get("http://127.0.0.1:8000/stations/")
        if station_response.status_code != 200:
            logger.error("Error fetching PAWS stations: %s", station_response.content)
            return

        stations = station_response.json()
        paws_stations = [station for station in stations if station['brand_name'] == "3D Paws"]

        if not paws_stations:
            logger.warning("No stations found for brand '3D Paws'.")
            return

        # Fetch sensor IDs
        sensor_response = requests.get("http://127.0.0.1:8000/sensors/")
        if sensor_response.status_code != 200:
            logger.error("Error fetching sensors: %s", sensor_response.content)
            return

        sensors = sensor_response.json()
        sensor_map = {sensor['type']: sensor['id'] for sensor in sensors}

        for station in paws_stations:
            self.stdout.write(f"  Fetching data for station: {station['name']} (ID: {station['id']})")
            raw_data = self.fetch_paws_station_data(portal_url, station['id'], start, end, user_email, api_key)
            if raw_data:
                saved_data = self.process_paws_data(station['id'], raw_data, sensor_map)
                self.stdout.write(self.style.SUCCESS(f"  Successfully processed {len(saved_data)} measurements"))
            else:
                self.stdout.write(self.style.ERROR(f"  Failed to fetch data"))

        self.stdout.write(self.style.SUCCESS("=== PAWS Data Fetch Complete ===\n"))

    def fetch_zentra_data(self):
        """Fetch data from Zentra instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting Zentra Data Fetch ==='))

        # API Configuration
        BASE_URL = "https://zentracloud.com/api/v4/get_readings/"
        API_TOKEN = "3db9d133d878433b0c7f4a26adfa566426921e0e"
        
        # Headers for API request
        headers = {"Authorization": f"Token {API_TOKEN}"}

        # Time range configuration for specific date
        current_date_start = datetime(2024, 12, 4).date()
        current_date_end = datetime(2024, 12, 4).date()

        START_DATE = datetime.combine(current_date_start, datetime.min.time())
        END_DATE = datetime.combine(current_date_end, datetime.min.time()) + timedelta(hours=23, minutes=59)

        # Get station info for Zentra brand
        station_response = requests.get("http://127.0.0.1:8000/stations/")
        if station_response.status_code != 200:
            logger.error("Error fetching Zentra stations: %s", station_response.content)
            return

        stations = station_response.json()
        zentra_stations = [station for station in stations if station['brand_name'] == "Zentra"]

        if not zentra_stations:
            logger.warning("No stations found for brand 'Zentra'.")
            return

        # Get sensor IDs
        sensor_response = requests.get("http://127.0.0.1:8000/sensors/")
        if sensor_response.status_code != 200:
            logger.error("Error fetching sensors: %s", sensor_response.content)
            return

        sensors = sensor_response.json()
        sensor_map = {sensor['type']: sensor['id'] for sensor in sensors}

        for station in zentra_stations:
            # Parameters for the API request
            base_params = {
                "device_sn": station['serial_number'],  # Use the station's serial number
                "start_date": START_DATE.strftime("%Y-%m-%d %H:%M:%S"),
                "end_date": END_DATE.strftime("%Y-%m-%d %H:%M:%S"),
                "output_format": "json",
                "per_page": 1000,
                "sort_by": "asc"
            }

            self.stdout.write(f"  Fetching data for station: {station['name']} (Device SN: {station['serial_number']})")
            
            all_data = {'data': {}}
            page = 1
            while True:
                params = {**base_params, 'page_num': page}
                response = self.fetch_zentra_station_data(BASE_URL, headers, params)
                
                if not response or 'data' not in response:
                    break
                    
                # Merge data from this page
                for measurement_name, measurement_data in response['data'].items():
                    if measurement_name not in all_data['data']:
                        all_data['data'][measurement_name] = []
                    all_data['data'][measurement_name].extend(measurement_data)
                
                # Check if we got less than the requested number of items
                total_readings = sum(len(data) for data in response['data'].values())
                if total_readings < base_params['per_page']:
                    break
                    
                page += 1
                self.stdout.write(f"  Fetched page {page-1}")

            if all_data['data']:
                saved_data = self.process_zentra_data(station['id'], all_data, sensor_map)
                self.stdout.write(self.style.SUCCESS(f"  Successfully processed {len(saved_data)} measurements"))
            else:
                self.stdout.write(self.style.ERROR(f"  Failed to fetch data"))

        self.stdout.write(self.style.SUCCESS("=== Zentra Data Fetch Complete ===\n"))

    def fetch_barani_data(self):
        """Fetch data from Barani instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting Barani Data Fetch ==='))

        # API Configuration
        BASE_URL = "https://api.allmeteo.com/api/historical_data"
        TOKEN = "yaoX9GFMP9ZUvxFej6LADSeF2LpccfF+qvYCpiT+LxA="
        
        # Headers for API request
        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }

        # Time range configuration for specific date
        current_date_start = datetime(2024, 12, 4).date()
        current_date_end = datetime(2024, 12, 4).date()

        START_DATE = datetime.combine(current_date_start, datetime.min.time())
        END_DATE = datetime.combine(current_date_end, datetime.min.time()) + timedelta(hours=23, minutes=59)

        # Convert to Unix timestamps
        params = {
            "from_time": int(START_DATE.timestamp()),
            "to_time": int(END_DATE.timestamp())
        }

        # Get station info for Allmeteo brand
        station_response = requests.get("http://127.0.0.1:8000/stations/")
        if station_response.status_code != 200:
            logger.error("Error fetching Barani stations: %s", station_response.content)
            return

        stations = station_response.json()
        barani_stations = [station for station in stations if station['brand_name'] == "Allmeteo"]

        if not barani_stations:
            logger.warning("No stations found for brand 'Allmeteo'.")
            return

        # Get sensor IDs
        sensor_response = requests.get("http://127.0.0.1:8000/sensors/")
        if sensor_response.status_code != 200:
            logger.error("Error fetching sensors: %s", sensor_response.content)
            return

        sensors = sensor_response.json()
        sensor_map = {sensor['type']: sensor['id'] for sensor in sensors}

        for station in barani_stations:
            # Prepare request body with station's device ID
            form_data = {
                "devices": (None, f'["{station["serial_number"]}"]')
            }

            self.stdout.write(f"  Fetching data for station: {station['name']} (Device ID: {station['serial_number']})")
            
            try:
                response = requests.post(
                    BASE_URL,
                    headers=headers,
                    params=params,
                    files=form_data
                )

                if response.status_code == 200:
                    data = response.json()
                    saved_data = self.process_barani_data(station['id'], data, sensor_map)
                    self.stdout.write(self.style.SUCCESS(f"  Successfully processed {len(saved_data)} measurements"))
                else:
                    self.stdout.write(self.style.ERROR(f"  Failed to fetch data. Status code: {response.status_code}"))
                    self.stdout.write(f"  Response content: {response.text}")

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"  Request error: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("=== Barani Data Fetch Complete ===\n"))

    def fetch_paws_station_data(self, portal_url, station_id, start, end, user_email, api_key):
        """Fetch data for a specific PAWS station"""
        url = f"{portal_url}/api/v1/data/{station_id}?start={start}&end={end}&email={user_email}&api_key={api_key}"
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching data for PAWS station %s: %s", station_id, e)
            return None

    def fetch_zentra_station_data(self, base_url, headers, params, max_retries=5, initial_delay=60):
        """Fetch data from Zentra API with retry logic"""
        for attempt in range(max_retries):
            try:
                self.stdout.write(f"  Attempt {attempt + 1} of {max_retries}")
                self.stdout.write(f"  Request URL: {base_url}")
                self.stdout.write(f"  Request params: {params}")
                response = requests.get(base_url, headers=headers, params=params)
                self.stdout.write(f"  Response status code: {response.status_code}")

                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS("  Successfully fetched data from Zentra API"))
                    response_data = response.json()
                    self.stdout.write("  Raw API Response:")
                    self.stdout.write(str(response_data)[:1000])  # Print first 1000 chars of response
                    return response_data
                elif response.status_code == 401:
                    self.stdout.write(self.style.ERROR("  Authentication failed. Please check your API token."))
                    self.stdout.write(f"  Response: {response.text}")
                    return None
                elif response.status_code == 403:
                    self.stdout.write(self.style.ERROR("  Forbidden. You might not have permission to access this resource."))
                    self.stdout.write(f"  Response: {response.text}")
                    return None
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', initial_delay))
                    self.stdout.write(self.style.WARNING(f"  Rate limit exceeded. Retrying in {retry_after} seconds..."))
                    time.sleep(retry_after)
                else:
                    self.stdout.write(self.style.ERROR(f"  Unexpected status code: {response.status_code}"))
                    if response.text:
                        self.stdout.write(f"  Response: {response.text}")
                    return None
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"  Request error: {str(e)}"))
                return None

        self.stdout.write(self.style.ERROR(f"  Max retries ({max_retries}) reached. Unable to fetch data."))
        return None

    def process_paws_data(self, station_id, raw_data, sensor_map):
        """Process and save PAWS data"""
        processed_data = []
        
        if isinstance(raw_data, dict):
            features = raw_data.get("features", [])
            
            if features:
                properties = features[0].get("properties", {})
                
                if "data" in properties:
                    data_entries = properties["data"]
                    measurements_by_hour = {}

                    # Group measurements by the nearest rounded hour
                    for entry in data_entries:
                        timestamp = entry["time"]
                        rounded_timestamp = self.round_to_nearest_hour(timestamp)
                        
                        if rounded_timestamp not in measurements_by_hour:
                            measurements_by_hour[rounded_timestamp] = []
                        measurements_by_hour[rounded_timestamp].append(entry)

                    # For each rounded hour, find and save the closest measurement
                    for rounded_hour, entries in measurements_by_hour.items():
                        closest_entry = self.get_closest_measurement(entries, rounded_hour)
                        if closest_entry:
                            measurements = closest_entry["measurements"]
                            is_test = closest_entry["test"] == "false"
                            for key, value in measurements.items():
                                sensor_id = sensor_map.get(key)
                                if sensor_id:
                                    Measurement.objects.create(
                                        station_id=station_id,
                                        sensor_id=sensor_id,
                                        date=rounded_hour.date(),
                                        time=rounded_hour.time(),
                                        value=value,
                                        status="successful",
                                        note="Data has been gathered",
                                        created_at=datetime.now()
                                    )
                                    processed_data.append(f"Saved PAWS measurement for station {station_id} at {rounded_hour}")
                else:
                    logger.warning("No 'data' field in PAWS properties")
            else:
                logger.warning("No features found in PAWS raw data")
        else:
            logger.warning("PAWS raw data is not a dictionary: %s", raw_data)

        return processed_data

    def process_zentra_data(self, station_id, response, sensor_map):
        """Process and save Zentra data"""
        if 'data' not in response:
            logger.error("No 'data' key found in the Zentra API response.")
            self.stdout.write(self.style.ERROR("Response structure:"))
            self.stdout.write(str(response)[:500])  # Print first 500 chars of response
            return []

        processed_data = []
        measurements_by_hour = {}

        # Process each measurement
        for measurement_name, measurement_data in response['data'].items():
            self.stdout.write(self.style.SUCCESS(f"\nProcessing measurement: {measurement_name}"))
            
            for config in measurement_data:
                metadata = config.get("metadata", {})
                readings = config.get("readings", [])
                
                # Process readings
                for reading in readings:
                    timestamp = self.parse_datetime(reading.get("datetime"))
                    if timestamp and reading.get("value") is not None:
                        rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                        
                        if rounded_timestamp not in measurements_by_hour:
                            measurements_by_hour[rounded_timestamp] = {}
                        
                        if measurement_name not in measurements_by_hour[rounded_timestamp]:
                            measurements_by_hour[rounded_timestamp][measurement_name] = []
                        
                        measurements_by_hour[rounded_timestamp][measurement_name].append({
                            'timestamp': timestamp,
                            'value': reading["value"]
                        })
                        self.stdout.write(f"Added reading: {reading['value']} at {timestamp} for {measurement_name}")

        # Process measurements by hour
        for rounded_hour, sensor_readings in measurements_by_hour.items():
            for sensor_type, readings in sensor_readings.items():
                # Get closest reading to rounded hour
                closest_reading = min(readings, key=lambda x: abs(x['timestamp'] - rounded_hour))
                
                sensor_id = sensor_map.get(sensor_type)
                if sensor_id:
                    try:
                        Measurement.objects.create(
                            station_id=station_id,
                            sensor_id=sensor_id,
                            date=rounded_hour.date(),
                            time=rounded_hour.time(),
                            value=closest_reading['value'],
                            status="successful",
                            note="Data has been gathered",
                            created_at=datetime.now()
                        )
                        processed_data.append(f"Saved Zentra measurement for station {station_id} at {rounded_hour}")
                    except Exception as e:
                        logger.error(f"Error saving measurement: {e}")
                        self.stdout.write(self.style.ERROR(f"Error saving measurement: {e}"))

        return processed_data

    def get_sensor_id(self, sensor_type):
        """Get sensor ID from the database"""
        try:
            sensor = Sensor.objects.get(type=sensor_type)
            return sensor.id
        except Sensor.DoesNotExist:
            return None

    def round_to_nearest_hour(self, timestamp_str):
        """Rounds the given timestamp to the nearest hour"""
        timestamp = parse_datetime(timestamp_str)
        if timestamp.minute >= 30:
            timestamp = timestamp.replace(minute=0) + timedelta(hours=1)
        else:
            timestamp = timestamp.replace(minute=0)
        return timestamp.replace(second=0, microsecond=0)

    def get_closest_measurement(self, entries, rounded_hour):
        """Find the closest measurement to the rounded hour"""
        closest_entry = None
        closest_time_diff = None
        for entry in entries:
            timestamp = parse_datetime(entry["time"])
            time_diff = abs(timestamp - rounded_hour)
            if closest_time_diff is None or time_diff < closest_time_diff:
                closest_time_diff = time_diff
                closest_entry = entry
        return closest_entry

    def parse_datetime(self, datetime_str):
        """Parse datetime string to timezone-aware datetime object"""
        if isinstance(datetime_str, str):
            try:
                parsed_datetime = parser.parse(datetime_str)
                if parsed_datetime.tzinfo is None:
                    parsed_datetime = timezone.make_aware(parsed_datetime, timezone.utc)
                return parsed_datetime
            except ValueError:
                logger.warning("Invalid datetime format: %s", datetime_str)
                return None
        elif isinstance(datetime_str, (int, float)):
            try:
                if datetime_str < 0 or datetime_str > 32503680000:
                    logger.warning("Invalid Unix timestamp value: %s", datetime_str)
                    return None
                timestamp = datetime.utcfromtimestamp(datetime_str)
                return timezone.make_aware(timestamp, timezone.utc)
            except (ValueError, OSError) as e:
                logger.warning("Invalid Unix timestamp value: %s (%s)", datetime_str, e)
                return None
        else:
            logger.warning("Invalid datetime value: %s", datetime_str)
            return None

    def process_barani_data(self, station_id, response_data, sensor_map):
        """Process and save Barani data"""
        processed_data = []
        measurements_by_hour = {}

        # Log the raw response for debugging
        self.stdout.write("Raw Barani response:")
        self.stdout.write(str(response_data)[:1000])  # First 1000 chars

        try:
            # The response data is a list of measurements
            if not isinstance(response_data, list):
                logger.error("Invalid response format from Barani API")
                return []

            # Group measurements by hour
            for reading in response_data:
                timestamp_str = reading.get('timestamp')
                if not timestamp_str:
                    continue

                timestamp = parse_datetime(timestamp_str)
                if not timestamp:
                    continue

                rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                
                if rounded_timestamp not in measurements_by_hour:
                    measurements_by_hour[rounded_timestamp] = {}

                # Process each field from the reading
                for field, value in reading.items():
                    # Skip non-measurement fields
                    if field in ['sn', 'timestamp', 'device_id']:
                        continue
                    
                    try:
                        # Convert value to float if it's a measurement
                        value = float(value)
                        
                        if field not in measurements_by_hour[rounded_timestamp]:
                            measurements_by_hour[rounded_timestamp][field] = []
                        
                        measurements_by_hour[rounded_timestamp][field].append({
                            'timestamp': timestamp,
                            'value': value
                        })
                        self.stdout.write(f"Added {field} reading: {value} at {timestamp}")
                    except (ValueError, TypeError):
                        # Skip fields that can't be converted to float
                        continue

            # Save measurements for each rounded hour
            for rounded_hour, sensor_readings in measurements_by_hour.items():
                for field, readings in sensor_readings.items():
                    # Get closest reading to rounded hour
                    closest_reading = min(readings, key=lambda x: abs(x['timestamp'] - rounded_hour))
                    
                    # Try to find a matching sensor in the database
                    for sensor_type, sensor_id in sensor_map.items():
                        if field.lower() in sensor_type.lower():
                            try:
                                Measurement.objects.create(
                                    station_id=station_id,
                                    sensor_id=sensor_id,
                                    date=rounded_hour.date(),
                                    time=rounded_hour.time(),
                                    value=closest_reading['value'],
                                    status="successful",
                                    note="Data has been gathered",
                                    created_at=datetime.now()
                                )
                                processed_data.append(f"Saved Barani measurement for station {station_id} at {rounded_hour}")
                                break  # Found a matching sensor, stop looking
                            except Exception as e:
                                logger.error(f"Error saving measurement: {e}")
                                self.stdout.write(self.style.ERROR(f"Error saving measurement: {e}"))

        except Exception as e:
            logger.error(f"Error processing Barani data: {e}")
            self.stdout.write(self.style.ERROR(f"Error processing Barani data: {e}"))

        return processed_data