#!/usr/bin/env python
"""
Check Allmeteo station configuration for wind vs helix stations
Run with: python check_allmeteo_stations.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def check_allmeteo_stations():
    print("=== ALLMETEO STATION ANALYSIS ===\n")
    
    # Get Allmeteo brand
    allmeteo_brand = Brand.objects.get(name='Allmeteo')
    allmeteo_stations = Station.objects.filter(brand=allmeteo_brand)
    
    print(f"Total Allmeteo stations: {allmeteo_stations.count()}")
    
    # Separate wind and helix stations
    wind_stations = []
    helix_stations = []
    
    for station in allmeteo_stations:
        if 'Wind' in station.name or 'MeteoWind' in station.name:
            wind_stations.append(station)
        elif 'Helix' in station.name or 'MeteoHelix' in station.name:
            helix_stations.append(station)
    
    print(f"\nWind Stations (MeteoWind): {len(wind_stations)}")
    for station in wind_stations:
        print(f"  - {station.name}")
    
    print(f"\nHelix Stations (MeteoHelix): {len(helix_stations)}")
    for station in helix_stations:
        print(f"  - {station.name}")
    
    # Check sensor types for each station type
    print(f"\n=== WIND STATION SENSORS ===")
    for station in wind_stations:
        print(f"\n{station.name}:")
        station_sensors = StationSensor.objects.filter(station=station)
        sensor_types = [ss.sensor.type for ss in station_sensors]
        for sensor_type in sensor_types:
            print(f"  - {sensor_type}")
        
        # Check measurements
        measurements = Measurement.objects.filter(station=station)
        print(f"  Total measurements: {measurements.count()}")
    
    print(f"\n=== HELIX STATION SENSORS ===")
    for station in helix_stations:
        print(f"\n{station.name}:")
        station_sensors = StationSensor.objects.filter(station=station)
        sensor_types = [ss.sensor.type for ss in station_sensors]
        for sensor_type in sensor_types:
            print(f"  - {sensor_type}")
        
        # Check measurements
        measurements = Measurement.objects.filter(station=station)
        print(f"  Total measurements: {measurements.count()}")
    
    # Check which sensors are wind-related
    print(f"\n=== WIND-RELATED SENSORS ===")
    wind_sensor_types = ['wind_ave10', 'wind_max10', 'wind_min10', 'dir_ave10', 'dir_max10', 'dir_hi10', 'dir_lo10']
    
    for sensor_type in wind_sensor_types:
        measurements = Measurement.objects.filter(
            station__brand=allmeteo_brand,
            sensor__type=sensor_type
        )
        stations_with_sensor = measurements.values_list('station__name', flat=True).distinct()
        print(f"\n{sensor_type}:")
        print(f"  Total measurements: {measurements.count()}")
        print(f"  Stations with data: {list(stations_with_sensor)}")
    
    print(f"\n=== END OF ANALYSIS ===")

if __name__ == "__main__":
    check_allmeteo_stations() 