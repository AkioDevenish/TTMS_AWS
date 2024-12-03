import requests
from django.core.management.base import BaseCommand
from paws.models import InstrumentMeasurement
from datetime import datetime
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Fetches data for instruments and stores it in the database'

    def handle(self, *args, **kwargs):
        portal_url = "http://3d-trinidad.icdp.ucar.edu"
        user_email = "jerome.ramirez@metoffice.gov.tt"
        api_key = "sVALwcRMyQmjtwYpDPW-"
        instrument_ids = [1, 2, 3]  # List of instrument IDs you want to fetch data for
        start_datetime = "2024-09-17 1:50:00"
        end_datetime = "2024-09-17 2:10:00"

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
                print("Response data:", response.json())  # Add this line to inspect the response
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for instrument {instrument_id}: {e}")
                return None

        def process_and_save_data(instrument_id, raw_data):
            processed_data = []
    
            # Assuming raw_data is a dictionary with a key "data" which is a list of entries
            if "data" in raw_data:
                for entry in raw_data["data"]:
                    timestamp = entry["time"]
                    is_test = entry["test"] == "false"
                    
                    measurements = entry["measurements"]
                    for key, value in measurements.items():
                        if key in measurement_mapping:
                            InstrumentMeasurement.objects.create(
                                name=f"Instrument {instrument_id}",
                                measurement_name=measurement_mapping[key]["name"],
                                value=value,
                                timestamp=timestamp,
                                is_test=is_test
                            )
                            processed_data.append(f"Saved: {measurement_mapping[key]['name']} - {value} at {timestamp}")
            else:
                print("Invalid response format:", raw_data)
            
            return processed_data

        all_saved_data = []
        for instrument_id in instrument_ids:
            raw_data = fetch_data(instrument_id)
            if raw_data:
                saved_data = process_and_save_data(instrument_id, raw_data)
                all_saved_data.extend(saved_data)
        
        self.stdout.write(self.style.SUCCESS(f"Data successfully saved: {all_saved_data}"))
