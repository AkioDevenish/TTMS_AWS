#!/usr/bin/env python
"""
Test timezone fix - show how times should be displayed
Run with: python test_timezone_fix.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Measurement, Brand
from django.utils import timezone
import datetime
import pytz

def test_timezone_fix():
    print("=== TIMEZONE FIX TEST ===\n")
    
    # Check current Django timezone
    print(f"Current Django timezone: {timezone.get_current_timezone()}")
    print(f"Current Django timezone name: {timezone.get_current_timezone_name()}")
    
    # Get current time in different formats
    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc)
    
    print(f"\nTime comparison:")
    print(f"UTC time: {now_utc}")
    print(f"Local time: {now_local}")
    print(f"Local time (formatted): {now_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Check OTT data with timezone conversion
    print(f"\n=== OTT DATA WITH TIMEZONE CONVERSION ===")
    
    ott_brand = Brand.objects.get(name='OTT')
    ott_stations = Station.objects.filter(brand=ott_brand)
    
    for station in ott_stations:
        print(f"\nStation: {station.name}")
        
        # Get latest measurement
        latest_measurement = Measurement.objects.filter(station=station).order_by('-date', '-time').first()
        
        if latest_measurement:
            # Create a datetime object from date and time
            measurement_dt = datetime.datetime.combine(latest_measurement.date, latest_measurement.time)
            
            # Make it timezone-aware (UTC)
            measurement_dt_utc = timezone.make_aware(measurement_dt, pytz.UTC)
            
            # Convert to local timezone
            measurement_dt_local = timezone.localtime(measurement_dt_utc)
            
            print(f"  Latest measurement:")
            print(f"    Raw date: {latest_measurement.date}")
            print(f"    Raw time: {latest_measurement.time}")
            print(f"    UTC datetime: {measurement_dt_utc}")
            print(f"    Local datetime: {measurement_dt_local}")
            print(f"    Local formatted: {measurement_dt_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"    Value: {latest_measurement.value}")
        else:
            print(f"  No measurements found")
    
    print(f"\n=== END OF TIMEZONE TEST ===")

if __name__ == "__main__":
    test_timezone_fix() 