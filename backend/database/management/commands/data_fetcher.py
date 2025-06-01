import requests
from django.core.management.base import BaseCommand
from database.models import Measurement, Station, Sensor, Brand, StationSensor, StationHealthLog
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from dateutil import parser
import logging
import time
from django.conf import settings
import os
from logging.handlers import RotatingFileHandler
import asyncio
import concurrent.futures

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
log_file = os.path.join(log_dir, 'fetcher.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)   
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Command(BaseCommand):
    help = 'Fetches data from PAWS, Zentra, and Barani instruments and stores it in the database'

    def handle(self, *args, **kwargs):
        logger.info("Starting data_fetcher management command")
        try:
            # Set Trinidad and Tobago timezone (UTC-4)
            tt_tz = timezone.get_fixed_timezone(-240)
            
            # Calculate time range from 12 hours ago to now
            end_time = timezone.now().astimezone(tt_tz)
            start_time = end_time - timedelta(hours=12)

            logger.info(f"Fetching data from {start_time} to {end_time}")

            # Format times for different APIs
            self.start_datetime = start_time.strftime("%Y-%m-%d %H:%M:%S")
            self.end_datetime = end_time.strftime("%Y-%m-%d %H:%M:%S")

            # Run fetchers concurrently (only OTT Hydromet active)
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                logger.info("Starting data fetchers")
                # Start all fetchers
                paws_future = executor.submit(self.fetch_paws_data)
                zentra_future = executor.submit(self.fetch_zentra_data)
                barani_future = executor.submit(self.fetch_barani_data)
                ott_future = executor.submit(self.fetch_ott_hydromet_data)

                # Wait for all fetchers to complete
                concurrent.futures.wait([paws_future, zentra_future, barani_future, ott_future])
                logger.info("All data fetchers completed")
                
        except Exception as e:
            logger.error(f"Error in data_fetcher command: {str(e)}")
            raise

    def get_stations_by_brand(self, brand_name):
        """Get stations by brand name directly from database"""
        return Station.objects.filter(brand__name=brand_name)

    def get_sensor_map(self):
        """Get sensor mapping directly from database"""
        sensors = Sensor.objects.all()
        return {sensor.type: sensor.id for sensor in sensors}

    def fetch_paws_data(self):
        """Fetch data from PAWS instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting PAWS Data Fetch ==='))
        
        # Use the same time range as defined in handle method
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)
        
        # Format times for PAWS API
        start = START_DATE.strftime("%Y-%m-%dT%H:%M:%S")
        end = END_DATE.strftime("%Y-%m-%dT%H:%M:%S")

        portal_url = "http://3d-trinidad.icdp.ucar.edu"
        user_email = "jerome.ramirez@metoffice.gov.tt"
        api_key = "sVALwcRMyQmjtwYpDPW-"

        # Get stations directly from database
        paws_stations = self.get_stations_by_brand("3D_Paws")
        if not paws_stations.exists():
            logger.warning("No stations found for brand '3D Paws'.")
            return

        sensor_map = self.get_sensor_map()

        for station in paws_stations:
            self.stdout.write(f"Fetching data for PAWS station: {station.name} (Serial: {station.serial_number})")
            
            # Use fetch_paws_station_data instead of direct API call
            data = self.fetch_paws_station_data(
                portal_url=portal_url,
                station_id=station.serial_number,  # Use serial_number instead of ID
                start=start,
                end=end,
                user_email=user_email,
                api_key=api_key
            )

            if data:
                try:
                    saved_data = self.process_paws_data(station.id, data, sensor_map)
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully processed data for station {station.name}"
                    ))
                except Exception as e:
                    logger.error(f"Error processing data for station {station.name}: {str(e)}")
            else:
                logger.warning(f"No data received for station {station.name}")

        self.stdout.write(self.style.SUCCESS("=== PAWS Data Fetch Complete ===\n"))

    def fetch_zentra_data(self):
        """Fetch data from Zentra instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting Zentra Data Fetch ==='))

        BASE_URL = "https://zentracloud.com/api/v4/get_readings/"
        API_TOKEN = "3db9d133d878433b0c7f4a26adfa566426921e0e"
        
        headers = {"Authorization": f"Token {API_TOKEN}"}

        # Use the same time range as defined in handle method
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)

        # Get stations directly from database
        zentra_stations = self.get_stations_by_brand("Zentra")
        if not zentra_stations.exists():
            logger.warning("No stations found for brand 'Zentra'.")
            return

        sensor_map = self.get_sensor_map()

        for station in zentra_stations:
            self.stdout.write(f"Fetching data for Zentra station: {station.name} (Serial: {station.serial_number})")
            if not station.serial_number:
                logger.warning(f"No serial number for station {station.name}")
                continue

            # Parameters for the API request
            base_params = {
                "device_sn": station.serial_number.strip(),  # Ensure clean serial number
                "start_date": START_DATE.strftime("%Y-%m-%d %H:%M:%S"),
                "end_date": END_DATE.strftime("%Y-%m-%d %H:%M:%S"),
                "output_format": "json",
                "per_page": 1000,
                "sort_by": "asc"
            }

            self.stdout.write(f"Time range: {base_params['start_date']} to {base_params['end_date']}")
            
            all_data = {'data': {}}
            page = 1
            data_found = False

            while True:
                params = {**base_params, 'page_num': page}
                response = self.fetch_zentra_station_data(BASE_URL, headers, params)
                
                if not response:
                    self.stdout.write(self.style.ERROR("No response received from API"))
                    break

                if 'data' not in response:
                    self.stdout.write(self.style.ERROR("No data field in response"))
                    self.stdout.write(f"Response structure: {response.keys()}")
                    break

                if not response['data']:
                    self.stdout.write(f"No data returned for page {page}")
                    if page == 1:
                        self.stdout.write("No measurements found in the specified time range")
                    break

                data_found = True
                # Rest of the processing remains the same
                for measurement_name, measurement_data in response['data'].items():
                    if measurement_name not in all_data['data']:
                        all_data['data'][measurement_name] = []
                    all_data['data'][measurement_name].extend(measurement_data)
                
                total_readings = sum(len(data) for data in response['data'].values())
                if total_readings < base_params['per_page']:
                    break
                    
                page += 1

            if data_found:
                saved_data = self.process_zentra_data(station.id, all_data, sensor_map)
                self.stdout.write(self.style.SUCCESS(f"Successfully processed {len(saved_data)} measurements"))
            else:
                self.stdout.write(self.style.WARNING("No data to process"))

        self.stdout.write(self.style.SUCCESS("=== Zentra Data Fetch Complete ===\n"))

    def fetch_barani_data(self):
        """Fetch data from Barani instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting Barani Data Fetch ==='))

        BASE_URL = "https://api.allmeteo.com/api/historical_data"
        TOKEN = "yaoX9GFMP9ZUvxFej6LADSeF2LpccfF+qvYCpiT+LxA="
        
        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }

        # Use the same time range as other fetchers
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)

        # Convert to Unix timestamps
        params = {
            "from_time": int(START_DATE.timestamp()),
            "to_time": int(END_DATE.timestamp())
        }

        # Get stations directly from database
        barani_stations = self.get_stations_by_brand("Allmeteo")
        if not barani_stations.exists():
            logger.warning("No stations found for brand 'Allmeteo'.")
            return

        sensor_map = self.get_sensor_map()

        for station in barani_stations:
            if not station.serial_number:
                logger.warning(f"No serial number for station {station.name}")
                continue

            # Prepare request body with station's device ID
            form_data = {
                "devices": (None, f'["{station.serial_number.strip()}"]')  # Ensure clean serial number
            }

            self.stdout.write(f"Fetcring data for Barani station: {station.name} (Serial: {station.serial_number})")
            
            try:
                response = requests.post(
                    BASE_URL,
                    headers=headers,
                    params=params,
                    files=form_data
                )

                if response.status_code == 200:
                    data = response.json()
                    saved_data = self.process_barani_data(station.id, data, sensor_map)
                    self.stdout.write(self.style.SUCCESS(f"  Successfully processed {len(saved_data)} measurements"))
                else:
                    self.stdout.write(self.style.ERROR(f"  Failed to fetch data. Status code: {response.status_code}"))
                    self.stdout.write(f"  Response content: {response.text}")

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"  Request error: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("=== Barani Data Fetch Complete ===\n"))

    def fetch_ott_hydromet_data(self):
        """Fetch data from OTT Hydromet instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting OTT Hydromet Data Fetch ==='))

        BASE_URL = "https://www.hydrometcloud.com/Data/rest/api/"
        API_KEY = "3235DzYLcYfYD1S8"
        CLIENT_ID = "207"
        HEADERS = {
            "api-key": API_KEY,
            "clientId": str(CLIENT_ID)
        }

        # Use the same time range as other fetchers
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)
        start_time = START_DATE.strftime("%Y-%m-%d %H:%M:%S")
        end_time = END_DATE.strftime("%Y-%m-%d %H:%M:%S")

        # List of station IDs and names
        stations = [
            {"id": 2303, "name": "POS_SAT"},
            {"id": 2304, "name": "SYNOP_SAT"},
            {"id": 2305, "name": "TOCO_SAT"},
        ]

        sensor_map = self.get_sensor_map()

        for station in stations:
            self.stdout.write(f"Fetching sensors for OTT station: {station['name']} ({station['id']})")
            sensors_url = f"{BASE_URL}sensors?stationId={station['id']}"
            sensors_resp = requests.get(sensors_url, headers=HEADERS)
            self.stdout.write(f"  Sensors API status: {sensors_resp.status_code}, response: {sensors_resp.text[:300]}")
            if sensors_resp.status_code != 200:
                self.stdout.write(self.style.ERROR(f"  Failed to fetch sensors. Status code: {sensors_resp.status_code}"))
                continue
            sensors = sensors_resp.json()
            for sensor in sensors:
                sensor_name = sensor['sensorName']
                self.stdout.write(f"  Fetching data for sensor: {sensor_name}")
                data_url = (
                    f"{BASE_URL}sensordata?stationId={station['id']}&sensorName={sensor_name}"
                    f"&startTime={start_time}&endTime={end_time}"
                )
                data_resp = requests.get(data_url, headers=HEADERS)
                self.stdout.write(f"    Data API status: {data_resp.status_code}, response: {data_resp.text[:300]}")
                if data_resp.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"    Failed to fetch data. Status code: {data_resp.status_code}"))
                    continue
                data = data_resp.json()
                # Save/process the data
                try:
                    processed = self.process_ott_hydromet_data(station['id'], sensor_name, data, sensor_map)
                    self.stdout.write(self.style.SUCCESS(f"    Successfully processed {len(processed)} measurements for {sensor_name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    Error processing data: {e}"))

        self.stdout.write(self.style.SUCCESS("=== OTT Hydromet Data Fetch Complete ===\n"))

    def fetch_paws_station_data(self, portal_url, station_id, start, end, user_email, api_key):
        """Fetch data for a specific PAWS station"""
        url = f"{portal_url}/api/v1/data/{station_id}?start={start}&end={end}&email={user_email}&api_key={api_key}"
        try:
            max_retries = 3
            retry_delay = 5  # seconds
            
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, verify=False, timeout=30)
                    
                    if response.status_code == 403:
                        logger.error(
                            f"Authentication failed for PAWS station {station_id}. "
                            f"Status: {response.status_code}, "
                            f"Response: {response.text[:200]}"  # Log first 200 chars of response
                        )
                        # Try to get historical data from database instead
                        historical_data = self.get_historical_data(station_id, start, end)
                        if historical_data:
                            logger.info(f"Using historical data for station {station_id}")
                            return historical_data
                        return None
                        
                    response.raise_for_status()
                    data = response.json()
                    
                    if not isinstance(data, dict) or 'features' not in data:
                        logger.error(f"Invalid data structure received for station {station_id}")
                        return None
                    
                    return data
                    
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        raise
                        
        except Exception as e:
            logger.error(f"Error fetching data for PAWS station {station_id}: {str(e)}")
            return None

    def get_historical_data(self, station_id, start, end):
        """Get historical data from database when API fails"""
        try:
            from database.models import Measurement
            
            measurements = Measurement.objects.filter(
                station_id=station_id,
                date__gte=start.split('T')[0],
                date__lte=end.split('T')[0]
            ).order_by('date', 'time')
            
            if measurements.exists():
                # Format data to match API response structure
                return {
                    'features': [{
                        'properties': {
                            'data': [{
                                'time': f"{m.date}T{m.time}",
                                'measurements': {
                                    m.sensor.type: m.value
                                }
                            } for m in measurements]
                        }
                    }]
                }
            return None
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
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
        measurements_by_hour = {}
        
        if isinstance(raw_data, dict):
            features = raw_data.get("features", [])
            self.stdout.write(f"Number of features: {len(features)}")
            
            if features:
                properties = features[0].get("properties", {})
                data_entries = properties.get("data", [])
                self.stdout.write(f"Number of data entries: {len(data_entries)}")
                
                # First, collect all measurements for each hour
                for entry in data_entries:
                    measurements = entry.get("measurements", {})
                    timestamp = entry.get("time")
                    
                    if timestamp and measurements:
                        # Parse timestamp without timezone adjustment
                        entry_time = parser.parse(timestamp)
                        rounded_hour = self.round_to_nearest_hour(entry_time.isoformat())
                        
                        if rounded_hour not in measurements_by_hour:
                            measurements_by_hour[rounded_hour] = {}
                        
                        for sensor_type, value in measurements.items():
                            if sensor_type not in measurements_by_hour[rounded_hour]:
                                measurements_by_hour[rounded_hour][sensor_type] = []
                            
                            measurements_by_hour[rounded_hour][sensor_type].append({
                                'timestamp': entry_time,
                                'value': value
                            })
                
                # Now process and save measurements for each hour
                for rounded_hour in measurements_by_hour:
                    for sensor_type, readings in measurements_by_hour[rounded_hour].items():
                        sensor_id = sensor_map.get(sensor_type)
                        if sensor_id:
                            # Ensure station-sensor relationship exists
                            self.ensure_station_sensor_relationship(station_id, sensor_id)
                            
                            # Get the reading closest to the rounded hour
                            closest_reading = min(readings, 
                                key=lambda x: abs(x['timestamp'] - rounded_hour))
                            
                            try:
                                Measurement.objects.create(
                                    station_id=station_id,
                                    sensor_id=sensor_id,
                                    date=rounded_hour.date(),
                                    time=rounded_hour.time(),
                                    value=closest_reading['value'],
                                    status="Successful",
                                    note="Data Acquired",
                                    created_at=timezone.now()
                                )
                                processed_data.append(
                                    f"Saved PAWS measurement for station {station_id} "
                                    f"sensor {sensor_type} at {rounded_hour}"
                                )
                                self.stdout.write(
                                    f"Saved measurement: {sensor_type} = {closest_reading['value']} "
                                    f"at {rounded_hour}"
                                )
                            except Exception as e:
                                logger.error(f"Error saving measurement: {e}")
                                self.stdout.write(self.style.ERROR(f"Error saving measurement: {e}"))
        
        # After processing measurements, process health data
        for rounded_hour in measurements_by_hour.keys():
            self.process_station_health(station_id, measurements_by_hour, rounded_hour, "3D_Paws")
        
        return processed_data

    def process_zentra_data(self, station_id, response_data, sensor_map):
        processed_data = []
        measurements_by_hour = {}

        try:
            # Process each measurement
            for measurement_name, measurement_data in response_data['data'].items():
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

            # Process measurements and health data for each hour
            for rounded_hour in measurements_by_hour.keys():
                # Process regular measurements
                for measurement_name, readings in measurements_by_hour[rounded_hour].items():
                    closest_reading = min(readings, key=lambda x: abs(x['timestamp'] - rounded_hour))
                    
                    sensor_id = sensor_map.get(measurement_name)
                    if sensor_id:
                        try:
                            self.ensure_station_sensor_relationship(station_id, sensor_id)
                            Measurement.objects.create(
                                station_id=station_id,
                                sensor_id=sensor_id,
                                date=rounded_hour.date(),
                                time=rounded_hour.time(),
                                value=closest_reading['value'],
                                status="Successful",
                                note="Data Acquired",
                                created_at=timezone.now()
                            )
                            processed_data.append(f"Saved measurement for station {station_id}")
                        except Exception as e:
                            logger.error(f"Error saving measurement: {e}")

                # Process health data for this hour
                self.process_station_health(station_id, measurements_by_hour, rounded_hour, "Zentra")

        except Exception as e:
            logger.error(f"Error processing data: {e}")

        return processed_data

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
                                self.ensure_station_sensor_relationship(station_id, sensor_id)
                                Measurement.objects.create(
                                    station_id=station_id,
                                    sensor_id=sensor_id,
                                    date=rounded_hour.date(),
                                    time=rounded_hour.time(),
                                    value=closest_reading['value'],
                                    status="Successful",
                                    note="Data Aquired",
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

        # After processing measurements, process health data
        for rounded_hour in measurements_by_hour.keys():
            self.process_station_health(station_id, measurements_by_hour, rounded_hour, "Allmeteo")

        return processed_data

    def process_ott_hydromet_data(self, station_id, sensor_name, data, sensor_map):
        """Process and save OTT Hydromet data, auto-creating Station and Sensor if missing"""
        processed_data = []
        measurements_by_hour = {}

        # --- Auto-create or update Station if missing (brand_id=3 for OTT) ---
        from database.models import Station, Sensor
        from django.utils import timezone
        ott_brand_id = 3
        # Try to get by serial_number first
        station_obj = Station.objects.filter(serial_number=str(station_id)).first()
        if not station_obj:
            station_obj = Station.objects.create(
                id=station_id,
                serial_number=str(station_id),
                name=str(station_id),
                brand_id=ott_brand_id,
                last_updated_at=timezone.now(),
                address='',
                installation_date=timezone.now().date(),
                created_at=timezone.now()
            )
        # Use the actual station id for all downstream logic
        station_id = station_obj.id

        try:
            # The data is expected to have a 'sensorData' key with a list of measurements
            sensor_data = data.get('sensorData', [])
            self.stdout.write(f"    Raw sensor_data for {sensor_name}: {sensor_data}")
            if not isinstance(sensor_data, list):
                self.stdout.write(self.style.ERROR(f"  sensorData missing or not a list for {sensor_name}"))
                return []

            for entry in sensor_data:
                timestamp_str = entry.get('sampleTime')
                value = entry.get('value')
                self.stdout.write(f"      Entry: sampleTime={timestamp_str}, value={value}")
                if not timestamp_str or value is None:
                    continue
                timestamp = self.parse_datetime(timestamp_str)
                if not timestamp:
                    continue
                rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                if rounded_timestamp not in measurements_by_hour:
                    measurements_by_hour[rounded_timestamp] = {}
                if sensor_name not in measurements_by_hour[rounded_timestamp]:
                    measurements_by_hour[rounded_timestamp][sensor_name] = []
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    continue
                measurements_by_hour[rounded_timestamp][sensor_name].append({
                    'timestamp': timestamp,
                    'value': value
                })

            # Save measurements for each rounded hour
            for rounded_hour, sensor_readings in measurements_by_hour.items():
                for field, readings in sensor_readings.items():
                    # --- Auto-create Sensor if missing ---
                    sensor_obj, created = Sensor.objects.get_or_create(
                        type=field,
                        unit=''
                    )
                    if created:
                        sensor_map[field] = sensor_obj.id
                    sensor_id = sensor_obj.id
                    # Get closest reading to rounded hour
                    closest_reading = min(readings, key=lambda x: abs(x['timestamp'] - rounded_hour))
                    try:
                        self.ensure_station_sensor_relationship(station_id, sensor_id)
                        Measurement.objects.create(
                            station_id=station_id,
                            sensor_id=sensor_id,
                            date=rounded_hour.date(),
                            time=rounded_hour.time(),
                            value=closest_reading['value'],
                            status="Successful",
                            note="Data Acquired",
                            created_at=timezone.now()
                        )
                        self.stdout.write(f"      Saved measurement: station_id={station_id}, sensor={field}, value={closest_reading['value']}, time={rounded_hour}")
                        processed_data.append(f"Saved OTT Hydromet measurement for station {station_id} at {rounded_hour}")
                    except Exception as e:
                        logger.error(f"Error saving measurement: {e}")
                        self.stdout.write(self.style.ERROR(f"Error saving measurement: {e}"))

            # After processing measurements, process health data
            for rounded_hour in measurements_by_hour.keys():
                self.process_station_health(station_id, measurements_by_hour, rounded_hour, "OTT")

        except Exception as e:
            logger.error(f"Error processing OTT Hydromet data: {e}")
            self.stdout.write(self.style.ERROR(f"Error processing OTT Hydromet data: {e}"))

        return processed_data

    def ensure_station_sensor_relationship(self, station_id, sensor_id):
        """Ensure station-sensor relationship exists"""
        try:
            StationSensor.objects.get_or_create(
                station_id=station_id,
                sensor_id=sensor_id
            )
            self.stdout.write(f"Station-Sensor relationship verified for station {station_id} and sensor {sensor_id}")
        except Exception as e:
            logger.error(f"Error creating station-sensor relationship: {e}")

    def process_station_health(self, station_id, measurements_by_hour, rounded_hour, brand_name):
        """Process health-related measurements for a station"""
        try:
            # Initialize status values
            battery_status = "Unknown"
            connectivity_status = "Unknown"
            
            if rounded_hour in measurements_by_hour:
                # Handle different brands' sensor names
                if brand_name == "3D_Paws":
                    # Check CSS and BPC for 3D_Paws
                    if 'css' in measurements_by_hour[rounded_hour]:
                        css_reading = min(measurements_by_hour[rounded_hour]['css'], 
                                        key=lambda x: abs(x['timestamp'] - rounded_hour))
                        css_value = css_reading['value']
                        connectivity_status = self.get_connectivity_status(css_value)
                    
                    if 'bpc' in measurements_by_hour[rounded_hour]:
                        battery_reading = min(measurements_by_hour[rounded_hour]['bpc'], 
                                           key=lambda x: abs(x['timestamp'] - rounded_hour))
                        battery_status = f"{battery_reading['value']}%"
                        
                elif brand_name == "Zentra":
                    # Check Battery Percent for Zentra
                    if 'Battery Percent' in measurements_by_hour[rounded_hour]:
                        battery_reading = min(measurements_by_hour[rounded_hour]['Battery Percent'], 
                                           key=lambda x: abs(x['timestamp'] - rounded_hour))
                        battery_status = f"{battery_reading['value']}%"
                        
                elif brand_name == "Allmeteo":
                    # Check battery for Allmeteo
                    if 'battery' in measurements_by_hour[rounded_hour]:
                        battery_reading = min(measurements_by_hour[rounded_hour]['battery'], 
                                           key=lambda x: abs(x['timestamp'] - rounded_hour))
                        battery_status = f"{battery_reading['value']}%"
            
            # Create health log entry
            StationHealthLog.objects.create(
                station_id=station_id,
                battery_status=battery_status,
                connectivity_status=connectivity_status,
                created_at=rounded_hour
            )
                
        except Exception as e:
            logger.error(f"Error processing station health: {e}")
            self.stdout.write(self.style.ERROR(f"Error processing station health: {e}"))

    def get_connectivity_status(self, css_value):
        """Convert CSS value to connectivity status"""
        try:
            css_value = float(css_value)
            if css_value >= -70:
                return "Excellent"
            elif css_value >= -85:
                return "Good"
            elif css_value >= -100:
                return "Fair"
            else:
                return "Poor"
        except (TypeError, ValueError):
            return "Unknown"

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
        """Parse datetime string to Trinidad and Tobago timezone (UTC-4)"""
        tt_tz = timezone.get_fixed_timezone(-240)
        
        if isinstance(datetime_str, str):
            try:
                parsed_datetime = parser.parse(datetime_str)
                if parsed_datetime.tzinfo is None:
                    parsed_datetime = timezone.make_aware(parsed_datetime, tt_tz)
                return parsed_datetime.astimezone(tt_tz)
            except ValueError:
                logger.warning("Invalid datetime format: %s", datetime_str)
                return None
        elif isinstance(datetime_str, (int, float)):
            try:
                if datetime_str < 0 or datetime_str > 32503680000:
                    logger.warning("Invalid Unix timestamp value: %s", datetime_str)
                    return None
                timestamp = datetime.utcfromtimestamp(datetime_str)
                return timezone.make_aware(timestamp, tt_tz)
            except (ValueError, OSError) as e:
                logger.warning("Invalid Unix timestamp value: %s (%s)", datetime_str, e)
                return None
        else:
            logger.warning("Invalid datetime value: %s", datetime_str)
            return None