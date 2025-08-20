#!/usr/bin/env python
"""
Check station IDs to see why frontend is requesting wrong stations
Run with: python check_station_ids.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand

def check_station_ids():
    print("=== CHECKING STATION IDs ===\n")
    
    # Get 3D Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    
    # Check all 3D Paws stations
    paws_stations = Station.objects.filter(brand=paws_brand).order_by('id')
    print(f"Total 3D Paws stations: {paws_stations.count()}")
    
    print("\n3D Paws stations:")
    for station in paws_stations:
        measurements = Measurement.objects.filter(station=station).count()
        status = "✅ HAS DATA" if measurements > 0 else "❌ NO DATA"
        print(f"  ID {station.id}: {station.name} - {status} ({measurements:,} measurements)")
    
    # Check what the frontend is requesting
    print(f"\n=== FRONTEND REQUEST ANALYSIS ===")
    print("Frontend is requesting: station_ids=15,16,17,18,19,20,21,22,23,24...")
    
    # Check which stations these IDs correspond to
    requested_ids = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    print(f"\nChecking requested station IDs:")
    
    for station_id in requested_ids:
        try:
            station = Station.objects.get(id=station_id)
            measurements = Measurement.objects.filter(station=station).count()
            status = "✅ HAS DATA" if measurements > 0 else "❌ NO DATA"
            print(f"  ID {station_id}: {station.name} ({station.brand.name}) - {status}")
        except Station.DoesNotExist:
            print(f"  ID {station_id}: Station not found!")
    
    # Check if T10 Paramin is being requested
    t10_paramin = Station.objects.filter(name='T10 Paramin').first()
    if t10_paramin:
        print(f"\nT10 Paramin (which has data):")
        print(f"  ID: {t10_paramin.id}")
        print(f"  Brand: {t10_paramin.brand.name}")
        print(f"  Measurements: {Measurement.objects.filter(station=t10_paramin).count():,}")
        
        if t10_paramin.id not in requested_ids:
            print(f"  ❌ PROBLEM: T10 Paramin (ID {t10_paramin.id}) is NOT in the requested IDs!")
            print(f"  This is why you see 'No Data' - frontend is requesting wrong stations!")
    
    # Check what stations SHOULD be requested
    print(f"\n=== WHAT SHOULD BE REQUESTED ===")
    paws_stations_with_data = []
    for station in paws_stations:
        measurements = Measurement.objects.filter(station=station).count()
        if measurements > 0:
            paws_stations_with_data.append(station)
    
    if paws_stations_with_data:
        print(f"3D Paws stations WITH data (should be requested):")
        for station in paws_stations_with_data:
            print(f"  ID {station.id}: {station.name} ({measurements:,} measurements)")
    else:
        print("❌ NO 3D Paws stations have data!")
        print("This means the 3D Paws API is not working at all.")

if __name__ == "__main__":
    check_station_ids() 