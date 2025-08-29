#!/usr/bin/env python
"""
Check REAL OTT data - no sample data
Run with: python check_real_ott_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def check_real_ott_data():
    print("=== REAL OTT DATA CHECK (NO SAMPLE DATA) ===\n")
    
    # Get OTT brand
    ott_brand = Brand.objects.get(name='OTT')
    print(f"OTT Brand ID: {ott_brand.id}")
    
    # Get OTT stations
    ott_stations = Station.objects.filter(brand=ott_brand)
    print(f"OTT stations: {ott_stations.count()}")
    
    # Check total measurements
    total_measurements = Measurement.objects.filter(station__brand=ott_brand).count()
    print(f"Total OTT measurements: {total_measurements}")
    
    print("\n=== REAL MEASUREMENT COUNTS BY STATION ===")
    for station in ott_stations:
        station_measurements = Measurement.objects.filter(station=station).count()
        print(f"{station.name}: {station_measurements} measurements")
    
    # Check specific sensor types that should have data
    print("\n=== REAL SENSOR DATA ANALYSIS ===")
    
    sensor_types_to_check = ['5 min rain', 'Air Temperature', 'Barometric Pressure', 'Battery']
    
    for sensor_type in sensor_types_to_check:
        print(f"\nSensor type: '{sensor_type}'")
        
        # Check if this sensor type exists
        sensors = Sensor.objects.filter(type=sensor_type)
        if not sensors.exists():
            print(f"  ❌ Sensor type '{sensor_type}' NOT FOUND in database")
            continue
        
        # Check measurements for this sensor type across OTT stations
        measurements = Measurement.objects.filter(
            station__brand=ott_brand,
            sensor__type=sensor_type
        )
        
        total_count = measurements.count()
        print(f"  Total measurements: {total_count}")
        
        if total_count > 0:
            # Show real data by station
            for station in ott_stations:
                station_measurements = measurements.filter(station=station)
                station_count = station_measurements.count()
                
                if station_count > 0:
                    latest = station_measurements.order_by('-date', '-time').first()
                    print(f"    {station.name}: {station_count} measurements")
                    print(f"      Latest: {latest.value} at {latest.date} {latest.time}")
                else:
                    print(f"    {station.name}: 0 measurements")
        else:
            print(f"  ❌ No measurements found for sensor type '{sensor_type}'")
    
    # Check recent data (last 24 hours)
    print("\n=== RECENT DATA CHECK (LAST 24 HOURS) ===")
    
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    yesterday = now - timedelta(hours=24)
    
    recent_measurements = Measurement.objects.filter(
        station__brand=ott_brand,
        date__gte=yesterday.date()
    )
    
    print(f"Recent measurements (last 24 hours): {recent_measurements.count()}")
    
    if recent_measurements.exists():
        # Group by station
        for station in ott_stations:
            station_recent = recent_measurements.filter(station=station)
            if station_recent.exists():
                latest = station_recent.order_by('-date', '-time').first()
                print(f"  {station.name}: {station_recent.count()} recent measurements")
                print(f"    Latest: {latest.value} at {latest.date} {latest.time}")
            else:
                print(f"  {station.name}: No recent measurements")
    else:
        print("❌ No recent measurements found")
    
    print("\n=== END OF REAL DATA CHECK ===")

if __name__ == "__main__":
    check_real_ott_data() 