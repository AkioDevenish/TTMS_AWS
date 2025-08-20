#!/usr/bin/env python
"""
Test the new sensor mapping functionality
Run with: python test_sensor_mapping.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.views import MeasurementViewSet

def test_sensor_mapping():
    print("=== TESTING SENSOR MAPPING ===\n")
    
    # Create a viewset instance
    viewset = MeasurementViewSet()
    
    # Test sensor mapping
    test_cases = [
        'Wind Direction',
        'Temperature 1',
        'Pressure',
        'Wind Speed',
        'Precipitation',
        'Unknown Sensor'
    ]
    
    print("Testing sensor name mapping:")
    for sensor_name in test_cases:
        mapped = viewset.get_sensor_mapping(sensor_name)
        print(f"  '{sensor_name}' → '{mapped}'")
    
    # Test with T10 Paramin data
    print(f"\n=== TESTING WITH T10 PARAMIN DATA ===")
    
    from database.models import Station, Measurement
    
    station = Station.objects.filter(name='T10 Paramin').first()
    if station:
        print(f"Station: {station.name} (ID: {station.id})")
        
        # Test Wind Direction mapping
        frontend_name = 'Wind Direction'
        mapped_code = viewset.get_sensor_mapping(frontend_name)
        print(f"Frontend requests: '{frontend_name}'")
        print(f"Maps to: '{mapped_code}'")
        
        # Check if this sensor exists
        measurements = Measurement.objects.filter(
            station=station,
            sensor__type=mapped_code
        )
        print(f"Measurements found: {measurements.count():,}")
        
        if measurements.exists():
            latest = measurements.order_by('-date', '-time').first()
            print(f"Latest measurement: {latest.date} {latest.time} - Value: {latest.value}")
            print(f"✅ SUCCESS: Sensor mapping is working!")
        else:
            print(f"❌ FAILED: No measurements found for mapped sensor '{mapped_code}'")
    else:
        print("❌ T10 Paramin station not found!")

if __name__ == "__main__":
    test_sensor_mapping() 