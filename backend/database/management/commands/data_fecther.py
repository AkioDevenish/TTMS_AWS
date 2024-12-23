import requests
from django.core.management.base import BaseCommand
from database.models import Measurement, Station, Sensor
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Fetches data for instruments and stores it in the database'

    def handle(self, *args, **kwargs):
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
            print("Error fetching stations:", station_response.content)
            return

        stations = station_response.json()
        station_ids = [station['id'] for station in stations if station['brand_name'] == "3D Paws"]

        if not station_ids:
            print("No station IDs found for brand '3D Paws'.")
            return

        # Fetch sensor IDs
        sensor_response = requests.get("http://127.0.0.1:8000/sensors/")
        if sensor_response.status_code != 200:
            print("Error fetching sensors:", sensor_response.content)
            return

        sensors = sensor_response.json()
        sensor_map = {sensor['type']: sensor['id'] for sensor in sensors}  # Assuming 'type' is the key to match

        def fetch_data(station_id):
            url = f"{portal_url}/api/v1/data/{station_id}?start={start}&end={end}&email={user_email}&api_key={api_key}"
            try:
                response = requests.get(url, verify=False)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for station {station_id}: {e}")
                return None

        def round_to_nearest_hour(timestamp_str):
            """Rounds the given timestamp to the nearest hour"""
            timestamp = parse_datetime(timestamp_str)
            if timestamp.minute >= 30:
                timestamp = timestamp.replace(minute=0) + timedelta(hours=1)
            else:
                timestamp = timestamp.replace(minute=0)
            return timestamp.replace(second=0, microsecond=0)

        def get_closest_measurement(entries, rounded_hour):
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

        def process_and_save_data(station_id, raw_data):
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
                            rounded_timestamp = round_to_nearest_hour(timestamp)
                            
                            if rounded_timestamp not in measurements_by_hour:
                                measurements_by_hour[rounded_timestamp] = []
                            measurements_by_hour[rounded_timestamp].append(entry)

                        # Now, for each rounded hour, find and save the closest measurement
                        for rounded_hour, entries in measurements_by_hour.items():
                            closest_entry = get_closest_measurement(entries, rounded_hour)
                            if closest_entry:
                                measurements = closest_entry["measurements"]
                                is_test = closest_entry["test"] == "false"
                                for key, value in measurements.items():
                                    sensor_id = sensor_map.get(key)  # Match the sensor name to get the ID
                                    if sensor_id:  # Only create measurement if sensor_id is found
                                        # Create and save the measurement
                                        Measurement.objects.create(
                                            station_id=station_id,  # Use the station_id
                                            sensor_id=sensor_id,  # Use the matched sensor_id
                                            date=rounded_hour.date(),
                                            time=rounded_hour.time(),
                                            value=value,
                                            status="successful",
                                            note="Data has been gathered",
                                            created_at=datetime.now()
                                        )
                                        processed_data.append(f"Saved measurement for station {station_id} at {rounded_hour}")

                    else:
                        print("No 'data' field in properties")
                else:
                    print("No features found in raw data")
            else:
                print("Raw data is not a dictionary:", raw_data)

            return processed_data

        all_saved_data = []
        for station_id in station_ids:
            raw_data = fetch_data(station_id)
            if raw_data:
                saved_data = process_and_save_data(station_id, raw_data)
                all_saved_data.extend(saved_data)
        
        self.stdout.write(self.style.SUCCESS(f"Data successfully saved: {all_saved_data}")) 
