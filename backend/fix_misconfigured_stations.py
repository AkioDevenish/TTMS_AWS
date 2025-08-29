#!/usr/bin/env python
"""
Fix misconfigured stations that have the wrong brand
Run with: python fix_misconfigured_stations.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor

def fix_misconfigured_stations():
    print("=== FIXING MISCONFIGURED STATIONS ===\n")
    
    # Get brands
    paws_brand = Brand.objects.get(name='3D_Paws')
    ott_brand = Brand.objects.get(name='OTT')
    
    # Check all 3D Paws stations
    paws_stations = Station.objects.filter(brand=paws_brand)
    print(f"Total 3D Paws stations: {paws_stations.count()}")
    
    misconfigured_stations = []
    correct_stations = []
    
    for station in paws_stations:
        # Check what sensor types this station actually has data for
        measurements = Measurement.objects.filter(station=station)
        if measurements.exists():
            # Get unique sensor types from actual measurements
            actual_sensor_types = measurements.values_list('sensor__type', flat=True).distinct()
            
            # Check if these are 3D Paws sensors or OTT sensors
            paws_sensors = ['bt1', 'mt1', 'bp1', 'ws', 'wd', 'rg', 'sv1', 'si1', 'su1', 'wg', 'wgd', 'bcs', 'bpc', 'css', 'hth', 'bh1', 'cfr', 'ht1', 'hh1', 'wbgt', 'hi', 'sh1', 'wbt', 'st1']
            ott_sensors = ['Air Temperature', 'Wind Speed', 'Wind Direction', 'Barometric Pressure', 'Daily Rain', 'Gust Speed', 'Gust Direction', 'Relative Humidity', 'Dew Point', 'Solar Radiation', 'Battery', '5 min rain']
            
            paws_count = sum(1 for s in actual_sensor_types if s in paws_sensors)
            ott_count = sum(1 for s in actual_sensor_types if s in ott_sensors)
            
            if ott_count > paws_count:
                misconfigured_stations.append((station, 'OTT', actual_sensor_types))
            else:
                correct_stations.append((station, actual_sensor_types))
    
    print(f"\nCorrectly configured 3D Paws stations: {len(correct_stations)}")
    for station, sensor_types in correct_stations:
        print(f"  ✅ {station.name}: {len(sensor_types)} sensor types")
    
    print(f"\nMisconfigured stations (should be OTT): {len(misconfigured_stations)}")
    for station, correct_brand, sensor_types in misconfigured_stations:
        print(f"  ❌ {station.name}: Currently 3D_Paws, should be {correct_brand}")
        print(f"    Actual sensor types: {list(sensor_types)[:5]}...")
    
    # Fix misconfigured stations
    if misconfigured_stations:
        print(f"\n=== FIXING MISCONFIGURED STATIONS ===")
        
        for station, correct_brand, sensor_types in misconfigured_stations:
            if correct_brand == 'OTT':
                old_brand = station.brand.name
                station.brand = ott_brand
                station.save()
                print(f"  ✅ Fixed {station.name}: {old_brand} → {station.brand.name}")
            else:
                print(f"  ⚠️  {station.name}: Unknown brand type {correct_brand}")
    
    # Final check
    print(f"\n=== FINAL STATUS ===")
    paws_stations = Station.objects.filter(brand=paws_brand)
    paws_with_data = 0
    
    for station in paws_stations:
        measurements = Measurement.objects.filter(station=station)
        if measurements.exists():
            paws_with_data += 1
    
    print(f"3D Paws stations with data: {paws_with_data}")
    print(f"3D Paws stations total: {paws_stations.count()}")
    
    if paws_with_data == 0:
        print("\n❌ NO 3D Paws stations have data!")
        print("This means either:")
        print("1. All stations were misconfigured (fixed above)")
        print("2. The 3D Paws API is still not working")
        print("3. The stations need to be configured with correct 3D Paws sensors")

if __name__ == "__main__":
    fix_misconfigured_stations() 