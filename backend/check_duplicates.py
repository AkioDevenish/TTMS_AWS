#!/usr/bin/env python
"""
Check for duplicate station-sensor combinations
Run with: python check_duplicates.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def check_duplicates():
    print("=== CHECKING FOR DUPLICATE STATION-SENSOR COMBINATIONS ===\n")
    
    # Check OTT brand specifically
    ott_brand = Brand.objects.get(name='OTT')
    ott_stations = Station.objects.filter(brand=ott_brand)
    
    print("OTT Stations:")
    for station in ott_stations:
        print(f"  {station.name} (ID: {station.id})")
    
    print("\nChecking for duplicates...")
    
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Find actual duplicates
        cursor.execute("""
            SELECT station_id, sensor_id, COUNT(*) as count
            FROM station_sensors 
            WHERE station_id IN %s
            GROUP BY station_id, sensor_id 
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """, [tuple(ott_stations.values_list('id', flat=True))])
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"Found {len(duplicates)} duplicate combinations:")
            for station_id, sensor_id, count in duplicates:
                station = Station.objects.get(id=station_id)
                sensor = Sensor.objects.get(id=sensor_id)
                print(f"  Station: {station.name}, Sensor: {sensor.type} - {count} relationships")
        else:
            print("No duplicate combinations found")
    
    print("\nDetailed breakdown by station:")
    
    for station in ott_stations:
        print(f"\n--- {station.name} ---")
        
        # Get all relationships for this station
        relationships = StationSensor.objects.filter(station=station)
        
        # Group by sensor type
        sensor_groups = {}
        for rel in relationships:
            sensor_type = rel.sensor.type
            if sensor_type not in sensor_groups:
                sensor_groups[sensor_type] = []
            sensor_groups[sensor_type].append(rel.id)
        
        # Show sensors with multiple relationships
        for sensor_type, rel_ids in sensor_groups.items():
            if len(rel_ids) > 1:
                print(f"  {sensor_type}: {len(rel_ids)} relationships (IDs: {rel_ids[:5]}{'...' if len(rel_ids) > 5 else ''})")
            else:
                print(f"  {sensor_type}: 1 relationship")
    
    print("\n=== END OF DUPLICATE CHECK ===")

if __name__ == "__main__":
    check_duplicates() 