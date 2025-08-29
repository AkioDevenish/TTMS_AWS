#!/usr/bin/env python
"""
Detailed script to check OTT station relationships
Run with: python check_ott_details.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def check_ott_details():
    print("=== OTT STATION DETAILED CHECK ===\n")
    
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
        
        # Group by sensor type
        sensor_counts = {}
        for rel in relationships:
            sensor_type = rel.sensor.type
            if sensor_type not in sensor_counts:
                sensor_counts[sensor_type] = 0
            sensor_counts[sensor_type] += 1
        
        print("  Relationships by sensor type:")
        for sensor_type, count in sorted(sensor_counts.items()):
            print(f"    {sensor_type}: {count} relationships")
        
        # Check measurements
        measurements = Measurement.objects.filter(station=station)
        print(f"  Total measurements: {measurements.count()}")
        
        # Check if measurements exist for each sensor type
        print("  Sensors with measurements:")
        for sensor_type in sensor_counts.keys():
            sensor_measurements = Measurement.objects.filter(
                station=station,
                sensor__type=sensor_type
            ).count()
            print(f"    {sensor_type}: {sensor_measurements} measurements")
    
    print("\n=== SUMMARY ===")
    
    # Check total OTT relationships vs measurements
    total_ott_relationships = StationSensor.objects.filter(station__brand=ott_brand).count()
    total_ott_measurements = Measurement.objects.filter(station__brand=ott_brand).count()
    
    print(f"Total OTT StationSensor relationships: {total_ott_relationships}")
    print(f"Total OTT measurements: {total_ott_measurements}")
    
    # Check for relationships without measurements
    relationships_without_measurements = 0
    for rel in StationSensor.objects.filter(station__brand=ott_brand):
        has_measurements = Measurement.objects.filter(
            station=rel.station,
            sensor=rel.sensor
        ).exists()
        if not has_measurements:
            relationships_without_measurements += 1
    
    print(f"OTT relationships WITHOUT measurements: {relationships_without_measurements}")
    print(f"OTT relationships WITH measurements: {total_ott_relationships - relationships_without_measurements}")
    
    print("\n=== END OF OTT CHECK ===")

if __name__ == "__main__":
    check_ott_details() 