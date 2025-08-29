#!/usr/bin/env python
"""
Test API timezone conversion
Run with: python test_api_timezone.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.views import MeasurementViewSet
from database.models import Station, Measurement, Brand
from django.utils import timezone
import datetime
import pytz

def test_api_timezone():
    print("=== API TIMEZONE CONVERSION TEST ===\n")
    
    # Test the convert_time_to_local method
    viewset = MeasurementViewSet()
    
    # Get OTT data
    ott_brand = Brand.objects.get(name='OTT')
    ott_station = Station.objects.filter(brand=ott_brand).first()
    
    if ott_station:
        print(f"Testing with station: {ott_station.name}")
        
        # Get latest measurement
        latest_measurement = Measurement.objects.filter(station=ott_station).order_by('-date', '-time').first()
        
        if latest_measurement:
            print(f"\nOriginal measurement:")
            print(f"  Date: {latest_measurement.date}")
            print(f"  Time: {latest_measurement.time}")
            print(f"  Value: {latest_measurement.value}")
            
            # Test the conversion method
            converted_time = viewset.convert_time_to_local(latest_measurement.date, latest_measurement.time)
            
            print(f"\nConverted time:")
            print(f"  Original time: {latest_measurement.time}")
            print(f"  Converted time: {converted_time}")
            
            # Manual verification
            measurement_dt = datetime.datetime.combine(latest_measurement.date, latest_measurement.time)
            measurement_dt_utc = timezone.make_aware(measurement_dt, pytz.UTC)
            measurement_dt_local = timezone.localtime(measurement_dt_utc)
            
            print(f"\nManual verification:")
            print(f"  UTC datetime: {measurement_dt_utc}")
            print(f"  Local datetime: {measurement_dt_local}")
            print(f"  Local time formatted: {measurement_dt_local.strftime('%H:%M:%S')}")
        else:
            print("No measurements found")
    else:
        print("No OTT stations found")
    
    print(f"\n=== END OF API TIMEZONE TEST ===")

if __name__ == "__main__":
    test_api_timezone() 