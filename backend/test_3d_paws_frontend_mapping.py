#!/usr/bin/env python
"""
Test 3D Paws frontend sensor mapping
Run with: python test_3d_paws_frontend_mapping.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor, Sensor

def test_3d_paws_frontend_mapping():
    print("=== 3D PAWS FRONTEND MAPPING TEST ===\n")
    
    # Get 3D Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    
    # Frontend sensor configuration (from your Vue file)
    frontend_config = {
        'bt1': { 'name': 'Temperature 1', 'unit': '°C' },
        'mt1': { 'name': 'Temperature 2', 'unit': '°C' },
        'bp1': { 'name': 'Pressure', 'unit': 'hPa' },
        'ws': { 'name': 'Wind Speed', 'unit': 'm/s' },
        'wd': { 'name': 'Wind Direction', 'unit': '°' },
        'rg': { 'name': 'Precipitation', 'unit': 'mm' },
        'sv1': { 'name': 'Downwelling Visible', 'unit': 'W/m²' },
        'si1': { 'name': 'Downwelling Infrared', 'unit': 'W/m²' },
        'su1': { 'name': 'Downwelling Ultraviolet', 'unit': 'W/m²' },
        'bpc': { 'name': 'Battery Percent', 'unit': '%' },
        'css': { 'name': 'Cell Signal Strength', 'unit': '%' }
    }
    
    # Database sensor types
    all_paws_sensor_relationships = StationSensor.objects.filter(station__brand=paws_brand)
    database_sensor_types = all_paws_sensor_relationships.values_list('sensor__type', flat=True).distinct()
    
    print("=== FRONTEND CONFIGURATION ===")
    print(f"Frontend shows {len(frontend_config)} sensors:")
    for sensor_code, config in frontend_config.items():
        print(f"  {sensor_code}: {config['name']} ({config['unit']})")
    
    print(f"\n=== DATABASE SENSOR TYPES ===")
    print(f"Database has {len(database_sensor_types)} sensor types:")
    for sensor_type in sorted(database_sensor_types):
        print(f"  {sensor_type}")
    
    print(f"\n=== MAPPING ANALYSIS ===")
    
    # Check which frontend sensors exist in database
    frontend_in_database = []
    frontend_not_in_database = []
    
    for sensor_code in frontend_config.keys():
        if sensor_code in database_sensor_types:
            frontend_in_database.append(sensor_code)
        else:
            frontend_not_in_database.append(sensor_code)
    
    print(f"Frontend sensors IN database: {len(frontend_in_database)}")
    for sensor in frontend_in_database:
        print(f"  ✅ {sensor}: {frontend_config[sensor]['name']}")
    
    if frontend_not_in_database:
        print(f"\nFrontend sensors NOT in database: {len(frontend_not_in_database)}")
        for sensor in frontend_not_in_database:
            print(f"  ❌ {sensor}: {frontend_config[sensor]['name']}")
    
    # Check which database sensors are missing from frontend
    database_not_in_frontend = []
    for sensor_type in database_sensor_types:
        if sensor_type not in frontend_config:
            database_not_in_frontend.append(sensor_type)
    
    if database_not_in_frontend:
        print(f"\nDatabase sensors NOT in frontend: {len(database_not_in_frontend)}")
        for sensor in database_not_in_frontend:
            print(f"  ❌ {sensor}")
    
    # Check measurements for each sensor type
    print(f"\n=== MEASUREMENT STATUS ===")
    for sensor_code in frontend_in_database:
        measurements = Measurement.objects.filter(
            station__brand=paws_brand,
            sensor__type=sensor_code
        ).count()
        print(f"  {sensor_code} ({frontend_config[sensor_code]['name']}): {measurements:,} measurements")
    
    # Check if there are any measurements at all
    total_measurements = Measurement.objects.filter(station__brand=paws_brand).count()
    print(f"\nTotal 3D Paws measurements: {total_measurements:,}")
    
    if total_measurements > 0:
        latest_measurement = Measurement.objects.filter(
            station__brand=paws_brand
        ).order_by('-date', '-time').first()
        
        print(f"Latest measurement: {latest_measurement.date} {latest_measurement.time}")
        print(f"Latest station: {latest_measurement.station.name}")
        print(f"Latest sensor: {latest_measurement.sensor.type}")

if __name__ == "__main__":
    test_3d_paws_frontend_mapping() 