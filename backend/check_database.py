#!/usr/bin/env python
"""
Simple script to check database state and StationSensor relationships
Run with: python check_database.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def check_database_state():
    print("=== DATABASE STATE CHECK ===\n")
    
    # Check brands
    print("BRANDS:")
    for brand in Brand.objects.all():
        print(f"  {brand.id}: {brand.name}")
    print()
    
    # Check stations by brand
    print("STATIONS BY BRAND:")
    for brand in Brand.objects.all():
        stations = Station.objects.filter(brand=brand)
        print(f"  {brand.name}: {stations.count()} stations")
        for station in stations[:3]:  # Show first 3 stations
            print(f"    - {station.name} (ID: {station.id})")
        if stations.count() > 3:
            print(f"    ... and {stations.count() - 3} more")
        print()
    
    # Check total StationSensor relationships
    total_relationships = StationSensor.objects.count()
    print(f"TOTAL StationSensor RELATIONSHIPS: {total_relationships}")
    
    # Check relationships by brand
    print("\nSTATIONSENSOR RELATIONSHIPS BY BRAND:")
    for brand in Brand.objects.all():
        brand_stations = Station.objects.filter(brand=brand)
        brand_relationships = StationSensor.objects.filter(station__in=brand_stations).count()
        print(f"  {brand.name}: {brand_relationships} relationships")
        
        # Show some examples
        if brand_relationships > 0:
            sample_relationships = StationSensor.objects.filter(
                station__in=brand_stations
            )[:5]  # Show first 5
            
            for rel in sample_relationships:
                print(f"    - Station: {rel.station.name}, Sensor: {rel.sensor.type}")
            
            if brand_relationships > 5:
                print(f"    ... and {brand_relationships - 5} more")
        print()
    
    # Check for duplicate relationships
    print("CHECKING FOR DUPLICATE RELATIONSHIPS:")
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT station_id, sensor_id, COUNT(*) as count
            FROM station_sensors 
            GROUP BY station_id, sensor_id 
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """)
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"  Found {len(duplicates)} duplicate relationship groups:")
            for station_id, sensor_id, count in duplicates[:10]:  # Show first 10
                print(f"    Station {station_id}, Sensor {sensor_id}: {count} relationships")
            
            if len(duplicates) > 10:
                print(f"    ... and {len(duplicates) - 10} more groups")
        else:
            print("  No duplicate relationships found")
    
    print()
    
    # Check measurements
    total_measurements = Measurement.objects.count()
    print(f"TOTAL MEASUREMENTS: {total_measurements}")
    
    # Check measurements by brand
    print("\nMEASUREMENTS BY BRAND:")
    for brand in Brand.objects.all():
        brand_stations = Station.objects.filter(brand=brand)
        brand_measurements = Measurement.objects.filter(station__in=brand_stations).count()
        print(f"  {brand.name}: {brand_measurements} measurements")
    
    print("\n=== END OF CHECK ===")

if __name__ == "__main__":
    check_database_state() 