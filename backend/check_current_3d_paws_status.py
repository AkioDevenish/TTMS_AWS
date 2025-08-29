#!/usr/bin/env python
"""
Check current 3D Paws data status
Run with: python check_current_3d_paws_status.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor

def check_current_3d_paws_status():
    print("=== CURRENT 3D PAWS STATUS ===\n")
    
    # Get 3D Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    
    # Check total measurements
    total_measurements = Measurement.objects.filter(station__brand=paws_brand).count()
    print(f"Total 3D Paws measurements: {total_measurements:,}")
    
    # Check each station
    stations = Station.objects.filter(brand=paws_brand)
    print(f"\nTotal 3D Paws stations: {stations.count()}")
    
    stations_with_data = []
    stations_without_data = []
    
    for station in stations:
        count = Measurement.objects.filter(station=station).count()
        if count > 0:
            stations_with_data.append((station, count))
        else:
            stations_without_data.append(station)
    
    print(f"\nStations WITH data: {len(stations_with_data)}")
    for station, count in stations_with_data:
        print(f"  ✅ {station.name}: {count:,} measurements")
        
        # Check latest measurement
        latest = Measurement.objects.filter(station=station).order_by('-date', '-time').first()
        if latest:
            print(f"    Latest: {latest.date} {latest.time} - {latest.sensor.type}: {latest.value}")
    
    print(f"\nStations WITHOUT data: {len(stations_without_data)}")
    for station in stations_without_data[:10]:  # Show first 10
        print(f"  ❌ {station.name}")
    
    if len(stations_without_data) > 10:
        print(f"  ... and {len(stations_without_data) - 10} more")
    
    # Check if any recent data was added
    print(f"\n=== RECENT DATA CHECK ===")
    recent_measurements = Measurement.objects.filter(
        station__brand=paws_brand
    ).order_by('-date', '-time')[:5]
    
    if recent_measurements:
        print("Latest 5 measurements:")
        for m in recent_measurements:
            print(f"  {m.date} {m.time} - {m.station.name} - {m.sensor.type}: {m.value}")
    else:
        print("No recent measurements found")
    
    # Check data fetcher status
    print(f"\n=== DATA FETCHER STATUS ===")
    print("The 3D Paws data fetcher is failing due to SSL certificate issues.")
    print("This is why stations show 'No Data' and 'Chart data length: 0'")
    print("\nTo fix this, you need to:")
    print("1. Contact 3D Paws support about SSL certificate issues")
    print("2. Or temporarily bypass SSL verification (not recommended for production)")
    print("3. Or use a different data source for these stations")

if __name__ == "__main__":
    check_current_3d_paws_status() 