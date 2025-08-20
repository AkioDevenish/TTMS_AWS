#!/usr/bin/env python
"""
Check 3D Paws sensor configuration and data issues
Run with: python check_3d_paws_sensors.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor, Sensor

def check_3d_paws_sensors():
    print("=== 3D PAWS SENSOR INVESTIGATION ===\n")
    
    # Get 3D Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    
    # Get all 3D Paws stations
    paws_stations = Station.objects.filter(brand=paws_brand)
    print(f"Total 3D Paws stations: {paws_stations.count()}")
    
    # List all stations
    print("\n=== 3D PAWS STATIONS ===")
    for station in paws_stations:
        print(f"  {station.id}: {station.name}")
    
    # Check StationSensor relationships for each station
    print("\n=== STATION-SENSOR RELATIONSHIPS ===")
    for station in paws_stations:
        print(f"\nStation: {station.name} (ID: {station.id})")
        station_sensors = StationSensor.objects.filter(station=station)
        print(f"  Configured sensors: {station_sensors.count()}")
        
        for ss in station_sensors:
            sensor = ss.sensor
            measurements = Measurement.objects.filter(station=station, sensor=sensor)
            count = measurements.count()
            print(f"    {sensor.type}: {count:,} measurements")
    
    # Get all sensor types configured for 3D Paws
    print("\n=== ALL 3D PAWS SENSOR TYPES ===")
    all_paws_sensor_relationships = StationSensor.objects.filter(station__brand=paws_brand)
    paws_sensor_types = all_paws_sensor_relationships.values_list('sensor__type', flat=True).distinct()
    
    print(f"Total sensor types configured: {len(paws_sensor_types)}")
    for sensor_type in sorted(paws_sensor_types):
        print(f"  {sensor_type}")
    
    # Check current frontend configuration
    print("\n=== CURRENT FRONTEND CONFIGURATION ===")
    frontend_sensors = [
        'Temperature 1', 'Temperature 2', 'Pressure', 'Wind Speed', 'Wind Direction',
        'Precipitation', 'Downwelling Visible', 'Downwelling Infrared', 'Downwelling Ultraviolet',
        'Battery Percent', 'Cell Signal Strength'
    ]
    
    print(f"Frontend shows {len(frontend_sensors)} sensors:")
    for sensor in frontend_sensors:
        print(f"  {sensor}")
    
    # Check for missing sensors
    print(f"\n=== MISSING SENSORS ===")
    missing_sensors = []
    for sensor_type in paws_sensor_types:
        if sensor_type not in frontend_sensors:
            missing_sensors.append(sensor_type)
    
    if missing_sensors:
        print(f"Found {len(missing_sensors)} sensors in database NOT in frontend:")
        for sensor in missing_sensors:
            print(f"  ❌ {sensor}")
    else:
        print("All database sensors are in frontend")
    
    # Check measurements for 3D Paws
    print(f"\n=== 3D PAWS DATA STATUS ===")
    total_measurements = Measurement.objects.filter(station__brand=paws_brand).count()
    print(f"Total 3D Paws measurements: {total_measurements:,}")
    
    if total_measurements > 0:
        latest_measurement = Measurement.objects.filter(
            station__brand=paws_brand
        ).order_by('-date', '-time').first()
        
        print(f"Latest measurement: {latest_measurement.date} {latest_measurement.time}")
        print(f"Latest station: {latest_measurement.station.name}")
        print(f"Latest sensor: {latest_measurement.sensor.type}")
    else:
        print("❌ NO MEASUREMENTS FOUND!")
    
    # Check if data fetcher is processing 3D Paws
    print(f"\n=== DATA FETCHER STATUS ===")
    print("Check if 3D Paws data fetcher is running in data_fetcher.py")

if __name__ == "__main__":
    check_3d_paws_sensors() 