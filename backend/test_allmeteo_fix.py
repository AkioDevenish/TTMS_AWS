#!/usr/bin/env python
"""
Test Allmeteo fix with wind vs helix station filtering
Run with: python test_allmeteo_fix.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand
from database.views import MeasurementViewSet

def test_allmeteo_fix():
    print("=== ALLMETEO FIX TEST ===\n")
    
    # Get Allmeteo brand
    allmeteo_brand = Brand.objects.get(name='Allmeteo')
    
    # Test wind sensor filtering
    print("=== TESTING WIND SENSOR FILTERING ===")
    wind_sensors = ['wind_Max10', 'wind_Min10', 'wdir_Max10']
    
    for sensor_type in wind_sensors:
        print(f"\nTesting sensor: {sensor_type}")
        
        # Get all stations with this sensor
        all_stations = Station.objects.filter(
            brand=allmeteo_brand,
            station_sensors__sensor__type=sensor_type
        ).distinct()
        
        # Get wind stations only
        wind_stations = all_stations.filter(name__icontains='Wind')
        
        print(f"  All stations with {sensor_type}: {all_stations.count()}")
        for station in all_stations:
            print(f"    - {station.name}")
        
        print(f"  Wind stations only: {wind_stations.count()}")
        for station in wind_stations:
            print(f"    - {station.name}")
            
            # Check measurements
            measurements = Measurement.objects.filter(
                station=station,
                sensor__type=sensor_type
            ).count()
            print(f"      Measurements: {measurements}")
    
    # Test non-wind sensor filtering
    print(f"\n=== TESTING NON-WIND SENSOR FILTERING ===")
    non_wind_sensors = ['temperature', 'humidity', 'pressure', 'irradiation']
    
    for sensor_type in non_wind_sensors:
        print(f"\nTesting sensor: {sensor_type}")
        
        # Get all stations with this sensor
        all_stations = Station.objects.filter(
            brand=allmeteo_brand,
            station_sensors__sensor__type=sensor_type
        ).distinct()
        
        # Get helix stations only
        helix_stations = all_stations.filter(name__icontains='Helix')
        
        print(f"  All stations with {sensor_type}: {all_stations.count()}")
        print(f"  Helix stations only: {helix_stations.count()}")
        for station in helix_stations:
            print(f"    - {station.name}")
            
            # Check measurements
            measurements = Measurement.objects.filter(
                station=station,
                sensor__type=sensor_type
            ).count()
            print(f"      Measurements: {measurements}")
    
    print(f"\n=== END OF ALLMETEO FIX TEST ===")

if __name__ == "__main__":
    test_allmeteo_fix() 