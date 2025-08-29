#!/usr/bin/env python
"""
Deep investigation of why Allmeteo sensors aren't getting data
Run with: python deep_allmeteo_investigation.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor, Sensor

def deep_allmeteo_investigation():
    print("=== DEEP ALLMETEO INVESTIGATION ===\n")
    
    # Get Allmeteo brand
    allmeteo_brand = Brand.objects.get(name='Allmeteo')
    
    # Get all Allmeteo stations
    allmeteo_stations = Station.objects.filter(brand=allmeteo_brand)
    print(f"Total Allmeteo stations: {allmeteo_stations.count()}")
    
    # List all stations
    print("\n=== ALLMETEO STATIONS ===")
    for station in allmeteo_stations:
        print(f"  {station.id}: {station.name}")
    
    # Check StationSensor relationships for each station
    print("\n=== STATION-SENSOR RELATIONSHIPS ===")
    for station in allmeteo_stations:
        print(f"\nStation: {station.name} (ID: {station.id})")
        station_sensors = StationSensor.objects.filter(station=station)
        print(f"  Configured sensors: {station_sensors.count()}")
        
        for ss in station_sensors:
            sensor = ss.sensor
            measurements = Measurement.objects.filter(station=station, sensor=sensor)
            count = measurements.count()
            print(f"    {sensor.type}: {count:,} measurements")
    
    # Check if sensors exist in Sensor table
    print("\n=== SENSOR TABLE CHECK ===")
    allmeteo_sensor_types = [
        'battery', 'dewPoint', 'humidity', 'irradiation', 'irradiation_max',
        'pressure', 'pressure_raw', 'rain', 'rainfall_rate_max', 'temperature',
        'temperature_max', 'temperature_min', 'temperature_wetbulb_stull2011_C',
        'wdir_Avg10', 'wdir_Gust10', 'wdir_Max10', 'wdir_Min10', 'wdir_Stdev10',
        'wind_Avg10', 'wind_Max10', 'wind_Min10', 'wind_Stdev10'
    ]
    
    for sensor_type in allmeteo_sensor_types:
        try:
            sensor = Sensor.objects.get(type=sensor_type)
            print(f"  ✅ {sensor_type}: Sensor ID {sensor.id}")
        except Sensor.DoesNotExist:
            print(f"  ❌ {sensor_type}: NOT FOUND in Sensor table!")
    
    # Check for any measurements at all for Allmeteo
    print("\n=== OVERALL ALLMETEO DATA CHECK ===")
    total_measurements = Measurement.objects.filter(station__brand=allmeteo_brand).count()
    print(f"Total Allmeteo measurements: {total_measurements:,}")
    
    # Check latest measurement timestamp
    latest_measurement = Measurement.objects.filter(
        station__brand=allmeteo_brand
    ).order_by('-date', '-time').first()
    
    if latest_measurement:
        print(f"Latest measurement: {latest_measurement.date} {latest_measurement.time}")
        print(f"Latest station: {latest_measurement.station.name}")
        print(f"Latest sensor: {latest_measurement.sensor.type}")
    else:
        print("No measurements found!")
    
    # Check if there are any measurements for the "missing" sensors
    print("\n=== CHECKING 'MISSING' SENSORS ===")
    missing_sensors = [
        'dewPoint', 'irradiation_max', 'pressure', 'rain', 'rainfall_rate_max',
        'temperature_wetbulb_stull2011_C', 'wdir_Avg10', 'wdir_Gust10',
        'wdir_Min10', 'wdir_Stdev10', 'wind_Avg10', 'wind_Stdev10'
    ]
    
    for sensor_type in missing_sensors:
        try:
            sensor = Sensor.objects.get(type=sensor_type)
            # Check if ANY station has this sensor configured
            stations_with_sensor = StationSensor.objects.filter(sensor=sensor)
            print(f"\n  {sensor_type}:")
            print(f"    Sensor ID: {sensor.id}")
            print(f"    Configured on stations: {stations_with_sensor.count()}")
            
            if stations_with_sensor.exists():
                for ss in stations_with_sensor:
                    station = ss.station
                    measurements = Measurement.objects.filter(station=station, sensor=sensor)
                    count = measurements.count()
                    print(f"      {station.name}: {count:,} measurements")
            else:
                print(f"    ❌ NOT configured on ANY station!")
                
        except Sensor.DoesNotExist:
            print(f"  ❌ {sensor_type}: Sensor not found in database!")

if __name__ == "__main__":
    deep_allmeteo_investigation() 