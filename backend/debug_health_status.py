#!/usr/bin/env python
"""
Debug why Station Health dashboard shows stations as offline
Run with: python debug_health_status.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Brand, StationHealthLog, Measurement
from django.utils import timezone
from datetime import timedelta

def debug_health_status():
    print("=== DEBUGGING STATION HEALTH STATUS ===\n")
    
    # Check the specific stations
    station_names = ['T14 UTT', 'T15 ASJA', 'T16 Lochmaben']
    
    for station_name in station_names:
        station = Station.objects.filter(name=station_name).first()
        if station:
            print(f"📍 {station.name}")
            print(f"   Brand: {station.brand.name}")
            print(f"   Current Brand ID: {station.brand.id}")
            
            # Check health logs
            health_logs = StationHealthLog.objects.filter(station=station)
            print(f"   Total Health Logs: {health_logs.count()}")
            
            if health_logs.exists():
                latest_log = health_logs.order_by('-created_at').first()
                print(f"   Latest Health Log: {latest_log.created_at}")
                print(f"   Battery Status: '{latest_log.battery_status}'")
                print(f"   Connectivity Status: '{latest_log.connectivity_status}'")
                
                # Check if the log is recent (within 24 hours)
                now = timezone.now()
                time_diff = now - latest_log.created_at
                hours_ago = time_diff.total_seconds() / 3600
                print(f"   Hours since last health log: {hours_ago:.2f}")
                
                # Check measurements
                measurements = Measurement.objects.filter(station=station)
                recent_measurements = measurements.filter(
                    created_at__gte=now - timedelta(hours=24)
                )
                print(f"   Recent measurements (24h): {recent_measurements.count()}")
                
                if recent_measurements.exists():
                    latest_measurement = recent_measurements.order_by('-created_at').first()
                    print(f"   Latest measurement: {latest_measurement.created_at}")
                    print(f"   Sensor: {latest_measurement.sensor.type}")
                    print(f"   Value: {latest_measurement.value}")
                
                # Analyze why status might be offline
                print(f"   === STATUS ANALYSIS ===")
                
                # Check connectivity status logic
                if latest_log.connectivity_status and latest_log.connectivity_status not in ['Unknown', 'No Data']:
                    print(f"   Has connectivity status: {latest_log.connectivity_status}")
                    if latest_log.connectivity_status in ['Excellent', 'Good', 'Fair', 'Connected']:
                        print(f"   → Should be ONLINE (good connectivity)")
                    elif latest_log.connectivity_status in ['Poor', 'No Signal']:
                        print(f"   → Should be OFFLINE (poor connectivity)")
                    else:
                        print(f"   → Should be WARNING (unknown connectivity)")
                else:
                    print(f"   No connectivity status, checking battery logic...")
                    
                    # Check battery status logic
                    if latest_log.battery_status not in ['Unknown', 'No Data']:
                        print(f"   Has battery status: {latest_log.battery_status}")
                        if latest_log.battery_status in ['Excellent', 'Good', 'Fair']:
                            print(f"   → Should be ONLINE (good battery)")
                        else:
                            print(f"   → Should check data freshness")
                    else:
                        print(f"   No battery status, checking data freshness...")
                    
                    # Check data freshness
                    if latest_log.created_at:
                        if hours_ago < 24:
                            print(f"   → Should be ONLINE (recent data: {hours_ago:.2f}h ago)")
                        else:
                            print(f"   → Should be OFFLINE (old data: {hours_ago:.2f}h ago)")
                    else:
                        print(f"   → Should be OFFLINE (no timestamp)")
                
            else:
                print(f"   ❌ NO HEALTH LOGS FOUND!")
            
            print()
    
    # Check what the API endpoint would return
    print("=== API ENDPOINT SIMULATION ===")
    
    # Simulate the logic from aws_station_health_logs view
    for station_name in station_names:
        station = Station.objects.filter(name=station_name).first()
        if station:
            print(f"\n🔍 Simulating API logic for {station.name}:")
            
            # Get latest health log
            latest_log = StationHealthLog.objects.filter(station=station).order_by('-created_at').first()
            
            if latest_log:
                # Default status
                status = 'Offline'
                connectivity_status = latest_log.connectivity_status
                battery_status = latest_log.battery_status
                
                print(f"   Initial status: {status}")
                print(f"   Connectivity: {connectivity_status}")
                print(f"   Battery: {battery_status}")
                
                if connectivity_status and connectivity_status not in ['Unknown', 'No Data']:
                    if connectivity_status in ['Excellent', 'Good', 'Fair', 'Connected']:
                        status = 'Online'
                        print(f"   → Status changed to ONLINE (good connectivity)")
                    elif connectivity_status in ['Poor', 'No Signal']:
                        status = 'Offline'
                        print(f"   → Status remains OFFLINE (poor connectivity)")
                    else:
                        status = 'Warning'
                        print(f"   → Status changed to WARNING (unknown connectivity)")
                else:
                    print(f"   No connectivity status, checking battery...")
                    
                    if battery_status not in ['Unknown', 'No Data']:
                        if latest_log.created_at and (timezone.now() - latest_log.created_at).total_seconds() < 86400:
                            status = 'Online'
                            print(f"   → Status changed to ONLINE (recent battery data)")
                        else:
                            status = 'Warning'
                            print(f"   → Status changed to WARNING (old battery data)")
                    else:
                        if latest_log.created_at and (timezone.now() - latest_log.created_at).total_seconds() < 86400:
                            status = 'Online'
                            print(f"   → Status changed to ONLINE (recent data)")
                        else:
                            status = 'Offline'
                            print(f"   → Status remains OFFLINE (no recent data)")
                    
                    # Special case for good battery
                    if battery_status in ['Excellent', 'Good', 'Fair']:
                        status = 'Online'
                        print(f"   → Status forced to ONLINE (good battery)")
                
                print(f"   FINAL STATUS: {status}")
            else:
                print(f"   ❌ No health log found - would be OFFLINE")

if __name__ == "__main__":
    debug_health_status() 