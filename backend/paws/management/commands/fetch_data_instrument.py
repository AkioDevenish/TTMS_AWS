import requests
from django.core.management.base import BaseCommand
from paws.models import Measurements
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Fetches data for instruments and stores it in the database'

    def handle(self, *args, **kwargs):
        portal_url = "http://3d-trinidad.icdp.ucar.edu"
        user_email = "jerome.ramirez@metoffice.gov.tt"
        api_key = "sVALwcRMyQmjtwYpDPW-"
        instrument_ids = [1, 3, 4, 6, 11, 12, 18, 24, 27, 28, 29, 31, 32, 33, 36, 37, 38, 41, 42]  # List of instrument IDs you want to fetch data for
        start_datetime = "2024-12-04 0:00:00"
        end_datetime = "2024-12-04 23:59:59"

        start = parse_datetime(start_datetime).isoformat() + "Z"
        end = parse_datetime(end_datetime).isoformat() + "Z"

        measurement_mapping = {
            "bp1": {"name": "BMX280 Pressure", "units": "hPa", "full_name": "Air Pressure"},
            "bt1": {"name": "BMX280 Temperature", "units": "°C", "full_name": "Temperature"},
            "mt1": {"name": "MCP9808 Temperature", "units": "°C", "full_name": "Temperature"},
            "ws": {"name": "Wind Speed", "units": "m/s", "full_name": "Wind Speed"},
            "wd": {"name": "Wind Direction", "units": "°", "full_name": "Wind Direction"},
            "rg": {"name": "Rain Gauge", "units": "mm", "full_name": "Precipitation"},
            "sv1": {"name": "SI1145 Visible", "units": "W/m²", "full_name": "Downwelling Irradiance"},
            "si1": {"name": "SI1145 Infrared", "units": "W/m²", "full_name": "Downwelling Irradiance"},
            "su1": {"name": "SI1145 Ultraviolet", "units": "W/m²", "full_name": "Downwelling Irradiance"},
            "bpc": {"name": "Battery Percent Charge", "units": "%", "full_name": "State of Health"},
            "css": {"name": "Cell Signal Strength", "units": "%", "full_name": "State of Health"},
        }

        def fetch_data(instrument_id):
            url = f"{portal_url}/api/v1/data/{instrument_id}?start={start}&end={end}&email={user_email}&api_key={api_key}"
            try:
                response = requests.get(url, verify=False)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for instrument {instrument_id}: {e}")
                return None

        def round_to_nearest_hour(timestamp_str):
            """Rounds the given timestamp to the nearest hour"""
            timestamp = parse_datetime(timestamp_str)
            if timestamp.minute >= 30:
                timestamp = timestamp.replace(minute=0) + timedelta(hours=1)
            else:
                timestamp = timestamp.replace(minute=0)
            # Ensure that seconds and microseconds are also reset to 0
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

        def process_and_save_data(instrument_id, raw_data):
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
                                    if key in measurement_mapping:
                                        # Check if we have already saved a measurement for this hour and instrument
                                        existing_measurement = Measurements.objects.filter(
                                            timestamp=rounded_hour,
                                            name=f"Instrument {instrument_id}",
                                            measurement_name=measurement_mapping[key]["name"]
                                        ).first()

                                        if not existing_measurement:
                                            # Create and save the measurement only if it hasn't been saved yet
                                            Measurements.objects.create(
                                                name=f"Instrument {instrument_id}",
                                                measurement_name=measurement_mapping[key]["name"],
                                                value=value,
                                                timestamp=rounded_hour,
                                                is_test=is_test
                                            )
                                            processed_data.append(f"Saved: {measurement_mapping[key]['name']} - {value} at {rounded_hour}")
                                        else:
                                            processed_data.append(f"Already exists for {measurement_mapping[key]['name']} at {rounded_hour}")
                                    else:
                                        print("Invalid measurement key:", key)
                    else:
                        print("No 'data' field in properties")
                else:
                    print("No features found in raw data")
            else:
                print("Raw data is not a dictionary:", raw_data)

            return processed_data

        all_saved_data = []
        for instrument_id in instrument_ids:
            raw_data = fetch_data(instrument_id)
            if raw_data:
                saved_data = process_and_save_data(instrument_id, raw_data)
                all_saved_data.extend(saved_data)
        
        self.stdout.write(self.style.SUCCESS(f"Data successfully saved: {all_saved_data}"))
