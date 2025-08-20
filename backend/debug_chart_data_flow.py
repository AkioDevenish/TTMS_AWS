#!/usr/bin/env python
"""
Debug chart data flow - why charts aren't plotting despite having measurements
Run with: python debug_chart_data_flow.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand, StationSensor
from django.utils import timezone
from datetime import timedelta

def debug_chart_data_flow():
    print("=== DEBUGGING CHART DATA FLOW ===\n")
    
    # Get 3D Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    
    # Check a specific station that should have data
    station = Station.objects.filter(brand=paws_brand, name='T15 ASJA').first()
    if not station:
        print("❌ T15 ASJA station not found!")
        return
    
    print(f"Station: {station.name} (ID: {station.id})")
    
    # Check total measurements
    total_measurements = Measurement.objects.filter(station=station).count()
    print(f"Total measurements: {total_measurements:,}")
    
    # Check recent measurements (last 24 hours)
    one_day_ago = timezone.now() - timedelta(days=1)
    recent_measurements = Measurement.objects.filter(
        station=station,
        created_at__gte=one_day_ago
    ).order_by('-created_at')
    
    print(f"Recent measurements (last 24h): {recent_measurements.count()}")
    
    if recent_measurements.exists():
        print("\nLatest 5 measurements:")
        for m in recent_measurements[:5]:
            print(f"  {m.date} {m.time} - {m.sensor.type}: {m.value}")
    
    # Check sensor types for this station
    print(f"\n=== SENSOR TYPES FOR {station.name} ===")
    station_sensors = StationSensor.objects.filter(station=station)
    print(f"Configured sensors: {station_sensors.count()}")
    
    for ss in station_sensors:
        sensor = ss.sensor
        measurements = Measurement.objects.filter(station=station, sensor=sensor)
        count = measurements.count()
        latest = measurements.order_by('-date', '-time').first()
        
        print(f"  {sensor.type}: {count:,} measurements")
        if latest:
            print(f"    Latest: {latest.date} {latest.time} - Value: {latest.value}")
    
    # Check if measurements have proper date/time values
    print(f"\n=== MEASUREMENT DATE/TIME CHECK ===")
    sample_measurements = Measurement.objects.filter(station=station).order_by('-date', '-time')[:5]
    
    for m in sample_measurements:
        print(f"  {m.date} {m.time} - {m.sensor.type}: {m.value}")
        print(f"    created_at: {m.created_at}")
        print(f"    date field: {m.date} (type: {type(m.date)})")
        print(f"    time field: {m.time} (type: {type(m.time)})")
    
    # Check API endpoint data
    print(f"\n=== API ENDPOINT SIMULATION ===")
    print("Testing what the station_overview API would return:")
    
    # Simulate the API call logic
    from database.views import MeasurementViewSet
    from django.test import RequestFactory
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/api/measurements/station_overview/')
    request.user = None  # Mock user
    
    # Get the viewset
    viewset = MeasurementViewSet()
    viewset.request = request
    
    # Check if we can get station data
    try:
        # This is a simplified check - the actual API logic is more complex
        print("  API endpoint should return data for this station")
        print("  Check if the frontend is calling the correct endpoint")
        print("  Check if the sensor type filtering is working")
    except Exception as e:
        print(f"  Error simulating API: {e}")
    
    # Check frontend sensor configuration
    print(f"\n=== FRONTEND SENSOR CONFIG CHECK ===")
    print("Frontend should be configured for these sensors:")
    frontend_sensors = [
        'bt1', 'mt1', 'bp1', 'ws', 'wd', 'rg', 'sv1', 'si1', 'su1', 
        'bpc', 'css', 'wg', 'wgd', 'bcs', 'hth', 'bh1', 'cfr', 'ht1', 
        'hh1', 'wbgt', 'hi', 'sh1', 'wbt', 'st1'
    ]
    
    for sensor_type in frontend_sensors:
        if StationSensor.objects.filter(station=station, sensor__type=sensor_type).exists():
            measurements = Measurement.objects.filter(station=station, sensor__type=sensor_type).count()
            print(f"  ✅ {sensor_type}: {measurements:,} measurements")
        else:
            print(f"  ❌ {sensor_type}: Not configured")

if __name__ == "__main__":
    debug_chart_data_flow() 