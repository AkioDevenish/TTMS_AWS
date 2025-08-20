#!/usr/bin/env python
"""
Test OTT API response to see why charts aren't showing
Run with: python test_ott_api.py
"""

import os
import django
from django.db.models import Q

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def test_ott_api():
    print("=== TESTING OTT API RESPONSE ===\n")
    
    # Get OTT brand
    ott_brand = Brand.objects.get(name='OTT')
    print(f"OTT Brand ID: {ott_brand.id}")
    
    # Get OTT stations
    ott_stations = Station.objects.filter(brand=ott_brand)
    print(f"OTT stations found: {ott_stations.count()}")
    
    station_ids = [s.id for s in ott_stations]
    print(f"Station IDs: {station_ids}")
    
    # Test with a sensor type that should have data
    sensor_type = '5 min rain'
    print(f"\nTesting sensor type: {sensor_type}")
    
    # Check if measurements exist
    measurements = Measurement.objects.filter(
        station_id__in=station_ids, 
        sensor__type=sensor_type
    )
    print(f"Measurements found: {measurements.count()}")
    
    if measurements.exists():
        sample = measurements.first()
        print(f"Sample measurement:")
        print(f"  Station: {sample.station.name}")
        print(f"  Value: {sample.value}")
        print(f"  Date: {sample.date}")
        print(f"  Time: {sample.time}")
        print(f"  Sensor ID: {sample.sensor.id}")
        print(f"  Sensor Brand: {sample.sensor.brand.name if sample.sensor.brand else 'No brand'}")
    
    # Test the history endpoint logic
    print(f"\n=== TESTING HISTORY ENDPOINT LOGIC ===")
    
    # Simulate what the history endpoint does
    hours = 12
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    time_threshold = now - timedelta(hours=hours)
    threshold_date = time_threshold.date()
    threshold_time = time_threshold.time()
    
    print(f"Time threshold: {threshold_date} {threshold_time}")
    
    # Filter measurements by time
    recent_measurements = measurements.filter(
        (Q(date=threshold_date) & Q(time__gte=threshold_time)) | 
        (Q(date__gt=threshold_date))
    )
    
    print(f"Recent measurements (last {hours} hours): {recent_measurements.count()}")
    
    if recent_measurements.exists():
        recent_sample = recent_measurements.first()
        print(f"Most recent: {recent_sample.station.name} - {recent_sample.value} at {recent_sample.date} {recent_sample.time}")
    
    print("\n=== END OF TEST ===")

if __name__ == "__main__":
    test_ott_api() 