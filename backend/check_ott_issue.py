#!/usr/bin/env python
"""
Check OTT station issue - why no data is showing
Run with: python check_ott_issue.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def check_ott_issue():
    print("=== OTT STATION ISSUE ANALYSIS ===\n")
    
    # Get OTT brand
    ott_brand = Brand.objects.get(name='OTT')
    print(f"OTT Brand ID: {ott_brand.id}")
    
    # Get OTT stations
    ott_stations = Station.objects.filter(brand=ott_brand)
    print(f"OTT Stations: {ott_stations.count()}")
    
    for station in ott_stations:
        print(f"\n--- Station: {station.name} (ID: {station.id}) ---")
        
        # Get all relationships for this station
        relationships = StationSensor.objects.filter(station=station)
        print(f"  Total relationships: {relationships.count()}")
        
        # Check measurements
        measurements = Measurement.objects.filter(station=station)
        print(f"  Total measurements: {measurements.count()}")
        
        if measurements.exists():
            print("  Has measurements!")
            # Show some sample measurements
            sample_measurements = measurements[:3]
            for m in sample_measurements:
                print(f"    {m.sensor.type}: {m.value} at {m.date} {m.time}")
        else:
            print("  NO measurements found")
    
    print("\n=== CHECKING FOR DUPLICATE SENSORS ===")
    
    # Check for duplicate sensors
    sensor_types = ['5 min rain', 'Air Temperature', 'Barometric Pressure', 'Battery']
    for sensor_type in sensor_types:
        sensors = Sensor.objects.filter(type=sensor_type)
        print(f"\nSensor type '{sensor_type}': {sensors.count()} sensors")
        
        for sensor in sensors:
            brand_name = sensor.brand.name if sensor.brand else "No brand"
            print(f"  ID: {sensor.id}, Brand: {brand_name}")
    
    print("\n=== CHECKING OTT SENSOR BRANDS ===")
    
    # Check what brands OTT sensors are assigned to
    ott_sensor_types = ['5 min rain', 'Air Temperature', 'Barometric Pressure', 'Baro Tendency', 'Battery']
    for sensor_type in ott_sensor_types:
        sensors = Sensor.objects.filter(type=sensor_type)
        print(f"\nSensor type '{sensor_type}':")
        
        for sensor in sensors:
            brand_name = sensor.brand.name if sensor.brand else "No brand"
            print(f"  ID: {sensor.id}, Brand: {brand_name}")
    
    print("\n=== END OF ANALYSIS ===")

if __name__ == "__main__":
    check_ott_issue() 