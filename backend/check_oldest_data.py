#!/usr/bin/env python
"""
Check the oldest measurements in the database to see if there's historical data
Run with: python check_oldest_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, StationSensor, Sensor

def check_oldest_data():
    print("=== CHECKING OLDEST DATA IN DATABASE ===\n")
    
    # Check overall database
    print("Overall database:")
    oldest_measurement = Measurement.objects.order_by('date', 'time').first()
    newest_measurement = Measurement.objects.order_by('-date', '-time').first()
    
    if oldest_measurement:
        print(f"  Oldest measurement: {oldest_measurement.date} {oldest_measurement.time} - Station: {oldest_measurement.station.name}, Sensor: {oldest_measurement.sensor.type}, Value: {oldest_measurement.value}")
    else:
        print("  No measurements in database")
    
    if newest_measurement:
        print(f"  Newest measurement: {newest_measurement.date} {newest_measurement.time} - Station: {newest_measurement.station.name}, Sensor: {newest_measurement.sensor.type}, Value: {newest_measurement.value}")
    else:
        print("  No measurements in database")
    
    # Check 3D Paws stations specifically
    print(f"\n3D Paws stations:")
    paws_stations = Station.objects.filter(brand__name='3D_Paws')
    
    for station in paws_stations[:10]:  # Show first 10
        print(f"\nStation: {station.name} (ID: {station.id})")
        
        # Check if station has any measurements at all
        all_measurements = Measurement.objects.filter(station=station)
        total_count = all_measurements.count()
        
        if total_count > 0:
            oldest = all_measurements.order_by('date', 'time').first()
            newest = all_measurements.order_by('-date', '-time').first()
            
            print(f"  Total measurements: {total_count}")
            print(f"  Oldest: {oldest.date} {oldest.time} - Sensor: {oldest.sensor.type}, Value: {oldest.value}")
            print(f"  Newest: {newest.date} {newest.time} - Sensor: {newest.sensor.type}, Value: {newest.value}")
            
            # Check by sensor type
            sensor_data = {}
            for m in all_measurements:
                sensor_type = m.sensor.type
                if sensor_type not in sensor_data:
                    sensor_data[sensor_type] = []
                sensor_data[sensor_type].append(m)
            
            print(f"  Sensors with data:")
            for sensor_type, measurements in sensor_data.items():
                print(f"    {sensor_type}: {len(measurements)} measurements")
        else:
            print(f"  No measurements at all")
    
    # Check measurement counts by brand
    print(f"\n=== MEASUREMENT COUNTS BY BRAND ===\n")
    
    from django.db.models import Count
    brand_counts = Measurement.objects.values('station__brand__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for brand_data in brand_counts:
        brand_name = brand_data['station__brand__name']
        count = brand_data['count']
        print(f"{brand_name}: {count:,} measurements")
    
    # Check measurement counts by sensor type
    print(f"\n=== MEASUREMENT COUNTS BY SENSOR TYPE ===\n")
    
    sensor_counts = Measurement.objects.values('sensor__type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for sensor_data in sensor_counts[:20]:  # Show top 20
        sensor_type = sensor_data['sensor__type']
        count = sensor_data['count']
        print(f"{sensor_type}: {count:,} measurements")

if __name__ == "__main__":
    check_oldest_data() 