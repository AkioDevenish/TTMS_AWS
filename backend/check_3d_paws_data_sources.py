#!/usr/bin/env python
"""
Check why only T10 Paramin has data while other 3D Paws stations have none
Run with: python check_3d_paws_data_sources.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor, Sensor

def check_3d_paws_data_sources():
    print("=== 3D PAWS DATA SOURCE INVESTIGATION ===\n")
    
    # Get 3D Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    
    # Get all 3D Paws stations
    paws_stations = Station.objects.filter(brand=paws_brand)
    
    print("=== STATION DATA ANALYSIS ===")
    
    stations_with_data = []
    stations_without_data = []
    
    for station in paws_stations:
        total_measurements = Measurement.objects.filter(station=station).count()
        
        if total_measurements > 0:
            stations_with_data.append((station, total_measurements))
        else:
            stations_without_data.append(station)
    
    print(f"Stations WITH data: {len(stations_with_data)}")
    for station, count in stations_with_data:
        print(f"  ✅ {station.name}: {count:,} measurements")
        
        # Check which sensors have data
        station_sensors = StationSensor.objects.filter(station=station)
        for ss in station_sensors:
            sensor = ss.sensor
            measurements = Measurement.objects.filter(station=station, sensor=sensor).count()
            if measurements > 0:
                print(f"    {sensor.type}: {measurements:,} measurements")
    
    print(f"\nStations WITHOUT data: {len(stations_without_data)}")
    for station in stations_without_data:
        print(f"  ❌ {station.name}")
        
        # Check if they have serial numbers (needed for API calls)
        if station.serial_number:
            print(f"    Serial: {station.serial_number}")
        else:
            print(f"    ❌ NO SERIAL NUMBER!")
    
    # Check if there are any recent measurements
    print(f"\n=== RECENT DATA CHECK ===")
    recent_measurements = Measurement.objects.filter(
        station__brand=paws_brand
    ).order_by('-date', '-time')[:10]
    
    if recent_measurements:
        print("Latest 10 measurements:")
        for m in recent_measurements:
            print(f"  {m.date} {m.time} - {m.station.name} - {m.sensor.type}: {m.value}")
    else:
        print("No recent measurements found")
    
    # Check data fetcher status
    print(f"\n=== DATA FETCHER STATUS ===")
    print("The 3D Paws data fetcher should be running via:")
    print("1. Celery task: data_fetcher")
    print("2. Manual command: python manage.py data_fetcher")
    print("3. API endpoint: http://3d-trinidad.icdp.ucar.edu")
    
    # Check if stations have proper serial numbers for API calls
    print(f"\n=== SERIAL NUMBER CHECK ===")
    stations_with_serial = paws_stations.filter(serial_number__isnull=False).exclude(serial_number='')
    stations_without_serial = paws_stations.filter(serial_number__isnull=True) | paws_stations.filter(serial_number='')
    
    print(f"Stations WITH serial numbers: {stations_with_serial.count()}")
    for station in stations_with_serial:
        print(f"  ✅ {station.name}: {station.serial_number}")
    
    if stations_without_serial.exists():
        print(f"\nStations WITHOUT serial numbers: {stations_without_serial.count()}")
        for station in stations_without_serial:
            print(f"  ❌ {station.name}: No serial number")
            print(f"    This station cannot fetch data from the API!")

if __name__ == "__main__":
    check_3d_paws_data_sources() 