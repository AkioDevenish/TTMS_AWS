#!/usr/bin/env python
"""
Check T10 Paramin sensors to see why API isn't returning data
Run with: python check_t10_paramin_sensors.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor

def check_t10_paramin_sensors():
    print("=== CHECKING T10 PARAMIN SENSORS ===\n")
    
    # Get T10 Paramin station
    station = Station.objects.filter(name='T10 Paramin').first()
    if not station:
        print("❌ T10 Paramin station not found!")
        return
    
    print(f"Station: {station.name} (ID: {station.id})")
    print(f"Brand: {station.brand.name}")
    
    # Check configured sensors
    print(f"\n=== CONFIGURED SENSORS ===")
    station_sensors = StationSensor.objects.filter(station=station)
    print(f"Total configured sensors: {station_sensors.count()}")
    
    configured_sensor_types = []
    for ss in station_sensors:
        sensor = ss.sensor
        measurements = Measurement.objects.filter(station=station, sensor=sensor).count()
        configured_sensor_types.append(sensor.type)
        print(f"  ✅ {sensor.type}: {measurements:,} measurements")
    
    # Check what sensor types actually have data
    print(f"\n=== SENSOR TYPES WITH DATA ===")
    measurements = Measurement.objects.filter(station=station)
    actual_sensor_types = measurements.values_list('sensor__type', flat=True).distinct()
    
    print(f"Total sensor types with data: {len(actual_sensor_types)}")
    for sensor_type in sorted(actual_sensor_types):
        count = measurements.filter(sensor__type=sensor_type).count()
        print(f"  📊 {sensor_type}: {count:,} measurements")
    
    # Check if "Wind Direction" sensor exists
    wind_direction_sensors = ['wd', 'Wind Direction']
    print(f"\n=== WIND DIRECTION SENSOR CHECK ===")
    
    for sensor_name in wind_direction_sensors:
        if sensor_name in configured_sensor_types:
            print(f"  ✅ {sensor_name}: Configured")
        else:
            print(f"  ❌ {sensor_name}: NOT configured")
        
        if sensor_name in actual_sensor_types:
            print(f"  📊 {sensor_name}: Has data")
        else:
            print(f"  ❌ {sensor_name}: No data")
    
    # Check what the frontend is requesting
    print(f"\n=== FRONTEND REQUEST ANALYSIS ===")
    print("Frontend is requesting sensor type: 'Wind Direction'")
    print("But T10 Paramin has sensor type: 'wd' (not 'Wind Direction')")
    
    # Check if there's a mapping issue
    print(f"\n=== SENSOR MAPPING ISSUE ===")
    print("The frontend is requesting 'Wind Direction' but the database has 'wd'")
    print("This is why the API returns no data - sensor type mismatch!")
    
    # Check if we can find the right sensor
    wd_sensor = StationSensor.objects.filter(station=station, sensor__type='wd').first()
    if wd_sensor:
        print(f"\n✅ Found 'wd' sensor configured for T10 Paramin")
        measurements = Measurement.objects.filter(station=station, sensor__type='wd').count()
        print(f"   Measurements: {measurements:,}")
        
        if measurements > 0:
            latest = Measurement.objects.filter(station=station, sensor__type='wd').order_by('-date', '-time').first()
            print(f"   Latest: {latest.date} {latest.time} - Value: {latest.value}")
    else:
        print(f"\n❌ 'wd' sensor not configured for T10 Paramin")

if __name__ == "__main__":
    check_t10_paramin_sensors() 