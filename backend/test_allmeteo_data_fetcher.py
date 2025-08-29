#!/usr/bin/env python
"""
Test Allmeteo data fetcher to identify data saving issues
Run with: python test_allmeteo_data_fetcher.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor, Sensor
from database.management.commands.data_fetcher import Command

def test_allmeteo_data_fetcher():
    print("=== TESTING ALLMETEO DATA FETCHER ===\n")
    
    # Get Allmeteo brand
    allmeteo_brand = Brand.objects.get(name='Allmeteo')
    
    # Get all Allmeteo stations
    allmeteo_stations = Station.objects.filter(brand=allmeteo_brand)
    print(f"Total Allmeteo stations: {allmeteo_stations.count()}")
    
    # Test sensor mapping
    fetcher = Command()
    sensor_map = fetcher.get_sensor_map()
    
    print(f"\n=== SENSOR MAPPING ===")
    print(f"Total sensors in database: {len(sensor_map)}")
    
    # Check if Allmeteo sensors are in the map
    allmeteo_sensor_types = [
        'battery', 'dewPoint', 'humidity', 'irradiation', 'irradiation_max',
        'pressure', 'pressure_raw', 'rain', 'rainfall_rate_max', 'temperature',
        'temperature_max', 'temperature_min', 'temperature_wetbulb_stull2011_C',
        'wdir_Avg10', 'wdir_Gust10', 'wdir_Max10', 'wdir_Min10', 'wdir_Stdev10',
        'wind_Avg10', 'wind_Max10', 'wind_Min10', 'wind_Stdev10'
    ]
    
    print(f"\n=== ALLMETEO SENSOR CHECK ===")
    for sensor_type in allmeteo_sensor_types:
        if sensor_type in sensor_map:
            print(f"  ✅ {sensor_type}: Sensor ID {sensor_map[sensor_type]}")
        else:
            print(f"  ❌ {sensor_type}: NOT FOUND in sensor map!")
    
    # Test the sensor matching logic from the fetcher
    print(f"\n=== TESTING SENSOR MATCHING LOGIC ===")
    
    # Simulate CSV field names from your export
    csv_fields = [
        'battery (V)', 'dewPoint (°C)', 'humidity (%)', 'irradiation (W/m2)',
        'irradiation_max (W/m2)', 'pressure_raw (hPa)', 'rain (mm)', 
        'temperature (°C)', 'temperature_max (°C)', 'temperature_min (°C)',
        'rainfall_rate_max (mm/h)', 'pressure (hPa)', 'temperature_wetbulb_stull2011_C (°C)'
    ]
    
    print(f"CSV fields from your export:")
    for field in csv_fields:
        print(f"  {field}")
        
        # Test the matching logic used in the fetcher
        matched_sensor = None
        for sensor_type, sensor_id in sensor_map.items():
            if field.lower() in sensor_type.lower():
                matched_sensor = sensor_type
                break
        
        if matched_sensor:
            print(f"    → Matches database sensor: {matched_sensor}")
        else:
            print(f"    → ❌ NO MATCH FOUND!")
    
    # Check if there are any measurements at all
    print(f"\n=== CURRENT ALLMETEO DATA STATUS ===")
    total_measurements = Measurement.objects.filter(station__brand=allmeteo_brand).count()
    print(f"Total Allmeteo measurements in database: {total_measurements:,}")
    
    if total_measurements > 0:
        latest_measurement = Measurement.objects.filter(
            station__brand=allmeteo_brand
        ).order_by('-date', '-time').first()
        
        print(f"Latest measurement: {latest_measurement.date} {latest_measurement.time}")
        print(f"Latest station: {latest_measurement.station.name}")
        print(f"Latest sensor: {latest_measurement.sensor.type}")
    
    # Check if the data fetcher is actually running
    print(f"\n=== DATA FETCHER STATUS ===")
    print("The Allmeteo fetcher is called 'fetch_barani_data' in the data_fetcher.py")
    print("It should be running every hour via Celery")
    print("Check if the task is running with: python manage.py shell -c 'from database.tasks import data_fetcher; print(data_fetcher.delay())'")

if __name__ == "__main__":
    test_allmeteo_data_fetcher() 