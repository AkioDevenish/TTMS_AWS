#!/usr/bin/env python
"""
Check 3D Paws progress after SSL fix
Run with: python check_3d_paws_progress.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand

def check_3d_paws_progress():
    print("=== 3D PAWS PROGRESS CHECK ===\n")
    
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
    for station in stations_without_data:
        print(f"  ❌ {station.name}")
    
    # Check recent data (last hour)
    print(f"\n=== RECENT DATA (Last Hour) ===")
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_measurements = Measurement.objects.filter(
        station__brand=paws_brand,
        created_at__gte=one_hour_ago
    ).order_by('-created_at')[:10]
    
    if recent_measurements:
        print(f"Found {recent_measurements.count()} measurements in the last hour:")
        for m in recent_measurements:
            print(f"  {m.created_at} - {m.station.name} - {m.sensor.type}: {m.value}")
    else:
        print("No recent measurements in the last hour")
    
    # Check if data fetcher is still running
    print(f"\n=== DATA FETCHER STATUS ===")
    print("The data fetcher should be running and collecting data.")
    print("Check the process with: ps aux | grep data_fetcher")

if __name__ == "__main__":
    check_3d_paws_progress() 