#!/usr/bin/env python
"""
Complete analysis of all 22 Allmeteo sensors
Run with: python complete_allmeteo_analysis.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor

def complete_allmeteo_analysis():
    print("=== COMPLETE ALLMETEO SENSOR ANALYSIS ===\n")
    
    # Get Allmeteo brand
    allmeteo_brand = Brand.objects.get(name='Allmeteo')
    
    # Get all sensor types from StationSensor relationships
    all_sensor_relationships = StationSensor.objects.filter(station__brand=allmeteo_brand)
    sensor_types_from_relationships = all_sensor_relationships.values_list('sensor__type', flat=True).distinct()
    
    print(f"Total sensor types in relationships: {len(sensor_types_from_relationships)}")
    print("\n=== SENSOR ANALYSIS ===")
    
    sensors_with_data = []
    sensors_without_data = []
    
    for sensor_type in sorted(sensor_types_from_relationships):
        measurements = Measurement.objects.filter(
            station__brand=allmeteo_brand,
            sensor__type=sensor_type
        )
        count = measurements.count()
        
        if count > 0:
            sensors_with_data.append((sensor_type, count))
            print(f"  ✅ {sensor_type}: {count:,} measurements")
        else:
            sensors_without_data.append(sensor_type)
            print(f"  ❌ {sensor_type}: 0 measurements")
    
    print(f"\n=== SUMMARY ===")
    print(f"Sensors WITH data: {len(sensors_with_data)}")
    print(f"Sensors WITHOUT data: {len(sensors_without_data)}")
    
    print(f"\n=== SENSORS WITH DATA (should be in frontend) ===")
    for sensor_type, count in sensors_with_data:
        print(f"  '{sensor_type}': {{ name: '{sensor_type.replace('_', ' ').title()}', unit: 'UNIT' }},")
    
    print(f"\n=== SENSORS WITHOUT DATA (should NOT be in frontend) ===")
    for sensor_type in sensors_without_data:
        print(f"  {sensor_type}")
    
    print(f"\n=== WIND VS NON-WIND CATEGORIZATION ===")
    
    wind_sensors = []
    non_wind_sensors = []
    
    for sensor_type, count in sensors_with_data:
        if 'wind' in sensor_type.lower() or 'wdir' in sensor_type.lower():
            wind_sensors.append((sensor_type, count))
        else:
            non_wind_sensors.append((sensor_type, count))
    
    print(f"\nWind sensors (for Wind stations):")
    for sensor_type, count in wind_sensors:
        print(f"  {sensor_type}: {count:,} measurements")
    
    print(f"\nNon-wind sensors (for Helix stations):")
    for sensor_type, count in non_wind_sensors:
        print(f"  {sensor_type}: {count:,} measurements")
    
    print(f"\n=== END OF ANALYSIS ===")

if __name__ == "__main__":
    complete_allmeteo_analysis() 