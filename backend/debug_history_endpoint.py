#!/usr/bin/env python
"""
Debug the history endpoint to see why it's not returning data
Run with: python debug_history_endpoint.py
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

def debug_history_endpoint():
    print("=== DEBUGGING HISTORY ENDPOINT ===\n")
    
    # Simulate the history endpoint logic
    station_ids = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 31, 32, 33, 34]
    sensor_types = ['bt1']
    hours = 12
    
    print(f"Requested parameters:")
    print(f"  station_ids: {station_ids}")
    print(f"  sensor_type: {sensor_types}")
    print(f"  hours: {hours}")
    
    # Get stations
    stations = Station.objects.filter(id__in=station_ids).select_related('brand')
    print(f"\nFound {stations.count()} stations")
    
    # Check T10 Paramin specifically
    t10_paramin = Station.objects.filter(name='T10 Paramin').first()
    if t10_paramin:
        print(f"\nT10 Paramin (ID: {t10_paramin.id}):")
        print(f"  Brand: {t10_paramin.brand.name}")
        
        # Check total bt1 measurements
        total_bt1 = Measurement.objects.filter(
            station=t10_paramin,
            sensor__type='bt1'
        ).count()
        print(f"  Total bt1 measurements: {total_bt1:,}")
        
        if total_bt1 > 0:
            latest_bt1 = Measurement.objects.filter(
                station=t10_paramin,
                sensor__type='bt1'
            ).order_by('-date', '-time').first()
            print(f"  Latest bt1 measurement: {latest_bt1.date} {latest_bt1.time}")
    
    # Simulate the time filtering logic
    now = timezone.now()
    time_threshold = now - timedelta(hours=hours)
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
        print("\nSample measurements:")
        for m in measurements[:5]:
            print(f"  Station {m.station_id}: {m.sensor.type} = {m.value} at {m.date} {m.time}")
    else:
        print("\n❌ NO MEASUREMENTS FOUND!")
        
        # Check what's happening with T10 Paramin specifically
        print(f"\n=== DEBUGGING T10 PARAMIN ===")
        t10_measurements = Measurement.objects.filter(
            station=t10_paramin,
            sensor__type='bt1'
        )
        
        if t10_measurements.exists():
            print(f"T10 Paramin has {t10_measurements.count():,} bt1 measurements total")
            
            # Check the date range
            min_date = t10_measurements.aggregate(min_date=models.Min('date'))['min_date']
            max_date = t10_measurements.aggregate(max_date=models.Max('date'))['max_date']
            print(f"Date range: {min_date} to {max_date}")
            
            # Check if any are within the time threshold
            recent_measurements = t10_measurements.filter(
                (Q(date=threshold_date) & Q(time__gte=threshold_time)) | 
                (Q(date__gt=threshold_date))
            )
            print(f"Measurements within {hours} hours: {recent_measurements.count()}")
            
            if recent_measurements.exists():
                latest = recent_measurements.order_by('-date', '-time').first()
                print(f"Latest recent measurement: {latest.date} {latest.time}")
            else:
                print("❌ No recent measurements found!")
                print("This explains why the API returns empty data!")
        else:
            print("❌ T10 Paramin has no bt1 measurements at all!")

if __name__ == "__main__":
    debug_history_endpoint() 