#!/usr/bin/env python
"""
Check T14, T15, T16 station brand assignments
Run with: python check_t14_t15_t16_brands.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Brand, StationHealthLog
from django.utils import timezone
from datetime import timedelta

def check_t14_t15_t16_brands():
    print("=== CHECKING T14, T15, T16 STATION BRANDS ===\n")
    
    # Check specific stations mentioned in the issue
    station_names = ['T14 UTT', 'T15 ASJA', 'T16 Lochmaben']
    
    for station_name in station_names:
        station = Station.objects.filter(name=station_name).first()
        if station:
            print(f"📍 {station.name}")
            print(f"   ID: {station.id}")
            print(f"   Brand: {station.brand.name}")
            print(f"   Status: {station.status}")
            print(f"   Serial Number: {station.serial_number}")
            
            # Check if this station has health logs
            health_logs = StationHealthLog.objects.filter(station=station)
            print(f"   Health Logs: {health_logs.count()}")
            
            if health_logs.exists():
                latest_log = health_logs.order_by('-created_at').first()
                print(f"   Latest Health Log: {latest_log.created_at}")
                print(f"   Battery Status: {latest_log.battery_status}")
                print(f"   Connectivity Status: {latest_log.connectivity_status}")
            else:
                print("   Health Logs: None")
            
            print()
        else:
            print(f"❌ Station '{station_name}' not found!")
            print()
    
    # Check all brands to see what stations they contain
    print("=== ALL BRANDS AND THEIR STATIONS ===")
    
    for brand in Brand.objects.all():
        stations = Station.objects.filter(brand=brand).exclude(status='Decommissioned')
        print(f"\n{brand.name} ({stations.count()} stations):")
        
        for station in stations:
            # Check if this station has recent health data
            one_day_ago = timezone.now() - timedelta(days=1)
            recent_health = StationHealthLog.objects.filter(
                station=station,
                created_at__gte=one_day_ago
            ).exists()
            
            status_indicator = "🟢" if recent_health else "🔴"
            print(f"  {status_indicator} {station.name} (ID: {station.id})")
    
    # Check if there are any stations with similar names that might be causing confusion
    print(f"\n=== CHECKING FOR SIMILAR STATION NAMES ===")
    
    # Look for stations that start with T14, T15, T16
    for prefix in ['T14', 'T15', 'T16']:
        similar_stations = Station.objects.filter(name__startswith=prefix)
        if similar_stations.exists():
            print(f"\nStations starting with '{prefix}':")
            for station in similar_stations:
                print(f"  {station.name} -> Brand: {station.brand.name}")
    
    # Check the OTT brand specifically
    print(f"\n=== OTT BRAND DETAILED CHECK ===")
    ott_brand = Brand.objects.filter(name='OTT').first()
    if ott_brand:
        ott_stations = Station.objects.filter(brand=ott_brand).exclude(status='Decommissioned')
        print(f"OTT brand has {ott_stations.count()} active stations:")
        
        for station in ott_stations:
            print(f"  - {station.name} (ID: {station.id})")
            
            # Check health status
            one_day_ago = timezone.now() - timedelta(days=1)
            latest_health = StationHealthLog.objects.filter(
                station=station,
                created_at__gte=one_day_ago
            ).order_by('-created_at').first()
            
            if latest_health:
                print(f"    Health: {latest_health.battery_status} | {latest_health.connectivity_status}")
            else:
                print(f"    Health: No recent data")
    else:
        print("❌ OTT brand not found!")

if __name__ == "__main__":
    check_t14_t15_t16_brands() 