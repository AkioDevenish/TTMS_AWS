#!/usr/bin/env python
"""
Get all 22 Allmeteo sensors for frontend dropdown
Run with: python get_all_allmeteo_sensors.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor

def get_all_allmeteo_sensors():
    print("=== ALL 22 ALLMETEO SENSORS FOR FRONTEND DROPDOWN ===\n")
    
    # Get Allmeteo brand
    allmeteo_brand = Brand.objects.get(name='Allmeteo')
    
    # Get all sensor types from StationSensor relationships
    all_sensor_relationships = StationSensor.objects.filter(station__brand=allmeteo_brand)
    sensor_types_from_relationships = all_sensor_relationships.values_list('sensor__type', flat=True).distinct()
    
    print("Here's your complete frontend configuration for Allmeteo:")
    print("'Allmeteo': {")
    
    # Define proper units for each sensor type
    sensor_units = {
        'battery': '%',
        'dewPoint': '°C',
        'humidity': '%',
        'irradiation': 'W/m²',
        'irradiation_max': 'W/m²',
        'pressure': 'hPa',
        'pressure_raw': 'hPa',
        'rain': 'mm',
        'rainfall_rate_max': 'mm/h',
        'temperature': '°C',
        'temperature_max': '°C',
        'temperature_min': '°C',
        'temperature_wetbulb_stull2011_C': '°C',
        'wdir_Avg10': '°',
        'wdir_Gust10': '°',
        'wdir_Max10': '°',
        'wdir_Min10': '°',
        'wdir_Stdev10': '°',
        'wind_Avg10': 'm/s',
        'wind_Max10': 'm/s',
        'wind_Min10': 'm/s',
        'wind_Stdev10': 'm/s'
    }
    
    # Generate frontend config
    for sensor_type in sorted(sensor_types_from_relationships):
        unit = sensor_units.get(sensor_type, 'UNIT')
        # Convert sensor type to display name
        display_name = sensor_type.replace('_', ' ').title()
        if 'Wdir' in display_name:
            display_name = display_name.replace('Wdir', 'Wind Direction')
        elif 'Wind' in display_name:
            display_name = display_name.replace('Wind', 'Wind Speed')
        
        print(f"    '{sensor_type}': {{ name: '{display_name}', unit: '{unit}' }},")
    
    print("},")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total sensors: {len(sensor_types_from_relationships)}")
    print(f"Wind sensors: {len([s for s in sensor_types_from_relationships if 'wind' in s.lower() or 'wdir' in s.lower()])}")
    print(f"Non-wind sensors: {len([s for s in sensor_types_from_relationships if 'wind' not in s.lower() and 'wdir' not in s.lower()])}")

if __name__ == "__main__":
    get_all_allmeteo_sensors() 