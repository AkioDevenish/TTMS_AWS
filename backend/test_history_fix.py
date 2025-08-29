#!/usr/bin/env python
"""
Test if the history endpoint fix is working
Run with: python test_history_fix.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

def test_history_fix():
    print("=== TESTING HISTORY ENDPOINT FIX ===\n")
    
    # Simulate the FIXED history endpoint logic
    station_ids = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 31, 32, 33, 34]
    sensor_types = ['bt1']
    hours = 12
    
    print(f"Requested parameters:")
    print(f"  station_ids: {station_ids}")
    print(f"  sensor_type: {sensor_types}")
    print(f"  hours: {hours}")
    
    # Get stations and check for 3D Paws
    stations = Station.objects.filter(id__in=station_ids).select_related('brand')
    paws_stations = stations.filter(brand__name='3D_Paws')
    has_paws = paws_stations.exists()
    
    if has_paws:
        # For 3D Paws stations, use extended time range
        effective_hours = max(hours, 24 * 30)  # At least 30 days
        print(f"✅ 3D Paws stations detected, using extended time range: {effective_hours} hours")
    else:
        effective_hours = hours
        print(f"Using time range of {effective_hours} hours for non-3D Paws brands")
    
    # Apply time filtering
    now = timezone.now()
    time_threshold = now - timedelta(hours=effective_hours)
    threshold_date = time_threshold.date()
    threshold_time = time_threshold.time()
    
    print(f"\nTime filtering:")
    print(f"  Current time: {now}")
    print(f"  Time threshold: {threshold_date} {threshold_time}")
    print(f"  Looking for measurements from: {threshold_date} {threshold_time} onwards")
    
    # Check measurements with time filtering
    measurements = Measurement.objects.filter(
        station_id__in=station_ids,
        sensor__type__in=sensor_types
    ).filter(
        (Q(date=threshold_date) & Q(time__gte=threshold_time)) | 
        (Q(date__gt=threshold_date))
    ).order_by('station_id', 'sensor__type', 'date', 'time')
    
    print(f"\nMeasurements found with time filtering: {measurements.count()}")
    
    if measurements.exists():
        print("\n✅ SUCCESS: Measurements found!")
        print("\nSample measurements:")
        for m in measurements[:5]:
            station_name = Station.objects.get(id=m.station_id).name
            print(f"  {station_name} (ID {m.station_id}): {m.sensor.type} = {m.value} at {m.date} {m.time}")
        
        # Check T10 Paramin specifically
        t10_measurements = measurements.filter(station_id=24)
        if t10_measurements.exists():
            print(f"\n✅ T10 Paramin has {t10_measurements.count()} measurements in the extended time range!")
        else:
            print(f"\n❌ T10 Paramin still has no measurements in the extended time range")
    else:
        print("\n❌ STILL NO MEASUREMENTS FOUND!")
        print("The fix didn't work as expected.")

if __name__ == "__main__":
    test_history_fix() 