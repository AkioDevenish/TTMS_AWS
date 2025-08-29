#!/usr/bin/env python
"""
Test the API endpoints directly to see if they're returning data
Run with: python test_api_directly.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import RequestFactory
from database.views import MeasurementViewSet
from database.models import Station, Measurement

def test_api_directly():
    print("=== TESTING API ENDPOINTS DIRECTLY ===\n")
    
    # Create a mock request factory
    factory = RequestFactory()
    
    # Test 1: station_overview endpoint
    print("=== TEST 1: station_overview endpoint ===")
    request = factory.get('/api/measurements/station_overview/?brand=3D_Paws&sensor_type=Temperature%201')
    request.user = None  # Mock user
    
    viewset = MeasurementViewSet()
    viewset.request = request
    
    try:
        response = viewset.station_overview(request)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"Response data keys: {list(data.keys())}")
            print(f"Total stations: {data.get('total', 0)}")
            
            stations = data.get('stations', [])
            print(f"Stations returned: {len(stations)}")
            
            for station in stations[:3]:  # Show first 3
                print(f"  Station {station['id']}: {station['name']}")
                if station.get('latest_measurement'):
                    print(f"    Has latest measurement: {station['latest_measurement']['value']}")
                else:
                    print(f"    No latest measurement")
        else:
            print(f"Error response: {response.data}")
    except Exception as e:
        print(f"Error testing station_overview: {e}")
    
    # Test 2: history endpoint
    print(f"\n=== TEST 2: history endpoint ===")
    request = factory.get('/api/measurements/history/?station_ids=24&sensor_type=bt1&hours=12')
    request.user = None  # Mock user
    
    try:
        response = viewset.history(request)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            if isinstance(data, dict):
                measurements = data.get('measurements', [])
                print(f"Measurements returned: {len(measurements)}")
                
                if measurements:
                    print("Sample measurements:")
                    for m in measurements[:3]:
                        print(f"  Station {m['station_id']}: {m['sensor_type']} = {m['value']} at {m['date']} {m['time']}")
                else:
                    print("❌ No measurements returned!")
            else:
                print(f"Unexpected response format: {type(data)}")
                print(f"Response: {data}")
        else:
            print(f"Error response: {response.data}")
    except Exception as e:
        print(f"Error testing history: {e}")
    
    # Test 3: Check if T10 Paramin actually has data
    print(f"\n=== TEST 3: Database Check ===")
    t10_paramin = Station.objects.filter(name='T10 Paramin').first()
    if t10_paramin:
        print(f"T10 Paramin (ID: {t10_paramin.id})")
        print(f"Brand: {t10_paramin.brand.name}")
        
        # Check bt1 measurements
        bt1_measurements = Measurement.objects.filter(
            station=t10_paramin,
            sensor__type='bt1'
        )
        print(f"Total bt1 measurements: {bt1_measurements.count():,}")
        
        if bt1_measurements.exists():
            latest = bt1_measurements.order_by('-date', '-time').first()
            print(f"Latest bt1 measurement: {latest.date} {latest.time} - Value: {latest.value}")
            
            # Check if any are within 30 days
            from django.utils import timezone
            from datetime import timedelta
            
            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_measurements = bt1_measurements.filter(
                date__gte=thirty_days_ago.date()
            )
            print(f"Measurements within 30 days: {recent_measurements.count()}")
        else:
            print("❌ No bt1 measurements found!")
    else:
        print("❌ T10 Paramin station not found!")

if __name__ == "__main__":
    test_api_directly() 