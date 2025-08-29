#!/usr/bin/env python
"""
Check if Allmeteo frontend sensor configuration matches database
Run with: python check_allmeteo_sensor_mismatch.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand

def check_allmeteo_sensor_mismatch():
    print("=== ALLMETEO SENSOR CONFIGURATION CHECK ===\n")
    
    # Get Allmeteo brand
    allmeteo_brand = Brand.objects.get(name='Allmeteo')
    
    # Get actual sensors in database with measurements
    measurements = Measurement.objects.filter(station__brand=allmeteo_brand)
    actual_sensors = measurements.values_list('sensor__type', flat=True).distinct()
    
    print("ACTUAL SENSORS IN DATABASE (with measurements):")
    for sensor in sorted(actual_sensors):
        print(f"  ✅ {sensor}")
    
    # Frontend configured sensors (from what I can see in the code)
    frontend_sensors = {
        'wind_Max10': 'Wind Speed (Max)',
        'wind_Min10': 'Wind Speed (Min)', 
        'wdir_Max10': 'Wind Direction (Max)',
        'battery': 'Battery',
        'humidity': 'Humidity',
        'irradiation': 'Irradiation',
        'pressure_raw': 'Pressure (Raw)',
        'temperature': 'Temperature',
        'temperature_max': 'Temperature (Max)',
        'temperature_min': 'Temperature (Min)'
    }
    
    print(f"\nFRONTEND CONFIGURED SENSORS:")
    for sensor, name in frontend_sensors.items():
        print(f"  {'✅' if sensor in actual_sensors else '❌'} {sensor}: {name}")
    
    # Check for missing sensors
    missing_sensors = set(frontend_sensors.keys()) - set(actual_sensors)
    extra_sensors = set(actual_sensors) - set(frontend_sensors.keys())
    
    print(f"\n=== ANALYSIS ===")
    
    if missing_sensors:
        print(f"❌ MISSING SENSORS (configured but no data):")
        for sensor in sorted(missing_sensors):
            print(f"  - {sensor}: {frontend_sensors.get(sensor, 'Unknown')}")
    else:
        print("✅ All configured sensors have data")
    
    if extra_sensors:
        print(f"❌ EXTRA SENSORS (have data but not configured):")
        for sensor in sorted(extra_sensors):
            print(f"  - {sensor}")
    else:
        print("✅ All database sensors are configured")
    
    # Check measurement counts for each sensor
    print(f"\n=== MEASUREMENT COUNTS BY SENSOR ===")
    for sensor in sorted(actual_sensors):
        count = measurements.filter(sensor__type=sensor).count()
        configured = "✅" if sensor in frontend_sensors else "❌"
        print(f"  {configured} {sensor}: {count:,} measurements")
    
    print(f"\n=== END OF CHECK ===")

if __name__ == "__main__":
    check_allmeteo_sensor_mismatch() 