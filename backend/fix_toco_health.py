#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, StationHealthLog, Measurement
from datetime import datetime, timedelta
import pytz

def fix_toco_health():
    """Fix TOCO_SAT's health status by creating a new health log"""
    
    # Get TOCO_SAT station
    station = Station.objects.get(name='TOCO_SAT')
    print(f"Fixing health for {station.name}...")
    
    # Get recent battery measurements
    tt_tz = pytz.timezone('America/Port_of_Spain')
    now = tt_tz.localize(datetime.now())
    yesterday = now - timedelta(hours=24)
    
    battery_measurements = Measurement.objects.filter(
        station=station,
        sensor__type='Battery',
        date__gte=yesterday.date()
    ).order_by('-date', '-time')
    
    if battery_measurements.exists():
        latest_battery = battery_measurements.first()
        battery_status = f"Battery: {latest_battery.value}"
        connectivity_status = "Connected"
        
        print(f"Latest battery reading: {battery_status}")
        print(f"Setting connectivity to: {connectivity_status}")
        
        # Create new health log
        health_log = StationHealthLog.objects.create(
            station=station,
            battery_status=battery_status,
            connectivity_status=connectivity_status
        )
        
        print(f"Created new health log: {health_log.id}")
        print(f"Battery: {health_log.battery_status}")
        print(f"Connectivity: {health_log.connectivity_status}")
        print(f"Created: {health_log.created_at}")
        
        return True
    else:
        print("No recent battery measurements found")
        return False

if __name__ == "__main__":
    fix_toco_health() 