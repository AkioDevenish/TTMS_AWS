#!/usr/bin/env python
"""
Comprehensive OTT test to identify why charts aren't showing
Run with: python comprehensive_ott_test.py
"""

import os
import django
from django.db.models import Q

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand
from django.utils import timezone
from datetime import timedelta

def comprehensive_ott_test():
    print("=== COMPREHENSIVE OTT TEST ===\n")
    
    # 1. Check OTT brand and stations
    ott_brand = Brand.objects.get(name='OTT')
    print(f"1. OTT Brand ID: {ott_brand.id}")
    
    ott_stations = Station.objects.filter(brand=ott_brand)
    print(f"   OTT stations: {ott_stations.count()}")
    
    for station in ott_stations:
        print(f"   - {station.name} (ID: {station.id})")
    
    # 2. Check sensor relationships
    print(f"\n2. Sensor Relationships:")
    for station in ott_stations:
        station_sensors = StationSensor.objects.filter(station=station)
        print(f"   {station.name}: {station_sensors.count()} sensors")
    
    # 3. Check measurements
    print(f"\n3. Measurements:")
    total_measurements = Measurement.objects.filter(station__brand=ott_brand).count()
    print(f"   Total OTT measurements: {total_measurements}")
    
    for station in ott_stations:
        station_measurements = Measurement.objects.filter(station=station).count()
        print(f"   {station.name}: {station_measurements} measurements")
    
    # 4. Test specific sensor type
    sensor_type = '5 min rain'
    print(f"\n4. Testing sensor type: '{sensor_type}':")
    
    measurements = Measurement.objects.filter(
        station__brand=ott_brand,
        sensor__type=sensor_type
    )
    print(f"   Total measurements for '{sensor_type}': {measurements.count()}")
    
    if measurements.exists():
        latest = measurements.order_by('-date', '-time').first()
        print(f"   Latest measurement: {latest.station.name} - {latest.value} at {latest.date} {latest.time}")
    
    # 5. Test time filtering (like the history endpoint)
    print(f"\n5. Testing time filtering (last 12 hours):")
    
    now = timezone.now()
    time_threshold = now - timedelta(hours=12)
    threshold_date = time_threshold.date()
    threshold_time = time_threshold.time()
    
    print(f"   Time threshold: {threshold_date} {threshold_time}")
    
    recent_measurements = measurements.filter(
        (Q(date=threshold_date) & Q(time__gte=threshold_time)) | 
        (Q(date__gt=threshold_date))
    )
    
    print(f"   Recent measurements: {recent_measurements.count()}")
    
    if recent_measurements.exists():
        recent_sample = recent_measurements.first()
        print(f"   Sample recent: {recent_sample.station.name} - {recent_sample.value} at {recent_sample.date} {recent_sample.time}")
    
    # 6. Test station overview logic
    print(f"\n6. Testing station overview logic:")
    
    for station in ott_stations:
        latest_measurement = Measurement.objects.filter(
            station_id=station.id,
            sensor__type=sensor_type
        ).order_by('-date', '-time').first()
        
        if latest_measurement:
            print(f"   {station.name}: {latest_measurement.value} at {latest_measurement.date} {latest_measurement.time}")
        else:
            print(f"   {station.name}: No data found")
    
    # 7. Check if there are any data issues
    print(f"\n7. Data consistency check:")
    
    for station in ott_stations:
        station_measurements = Measurement.objects.filter(station=station)
        if station_measurements.exists():
            sensor_types = station_measurements.values_list('sensor__type', flat=True).distinct()
            print(f"   {station.name} has sensors: {list(sensor_types)[:5]}")
        else:
            print(f"   {station.name}: No measurements at all")
    
    print("\n=== END OF COMPREHENSIVE TEST ===")

if __name__ == "__main__":
    comprehensive_ott_test() 