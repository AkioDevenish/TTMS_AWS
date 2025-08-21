#!/usr/bin/env python
"""
Comprehensive investigation of T14, T15, T16 stations
Run with: python investigate_t14_t15_t16.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Brand, StationHealthLog, StationSensor, Sensor, Measurement
from django.utils import timezone
from datetime import timedelta

def investigate_t14_t15_t16():
    print("=== COMPREHENSIVE INVESTIGATION OF T14, T15, T16 STATIONS ===\n")
    
    # Check the specific stations
    station_names = ['T14 UTT', 'T15 ASJA', 'T16 Lochmaben']
    
    print("=== DETAILED STATION ANALYSIS ===")
    for station_name in station_names:
        station = Station.objects.filter(name=station_name).first()
        if station:
            print(f"\n📍 {station.name}")
            print(f"   ID: {station.id}")
            print(f"   Brand: {station.brand.name}")
            print(f"   Status: {station.status}")
            print(f"   Serial Number: {station.serial_number}")
            print(f"   Address: {station.address}")
            print(f"   Installation Date: {station.installation_date}")
            print(f"   Last Updated: {station.last_updated_at}")
            
            # Check sensor relationships
            station_sensors = StationSensor.objects.filter(station=station)
            print(f"   Configured Sensors: {station_sensors.count()}")
            
            for ss in station_sensors:
                sensor = ss.sensor
                print(f"     • {sensor.type} (Brand: {sensor.brand.name if sensor.brand else 'None'})")
            
            # Check measurements
            measurements = Measurement.objects.filter(station=station)
            print(f"   Total Measurements: {measurements.count()}")
            
            if measurements.exists():
                latest_measurement = measurements.order_by('-date', '-time').first()
                print(f"   Latest Measurement: {latest_measurement.date} {latest_measurement.time}")
                
                # Check measurements by sensor type
                sensor_measurements = {}
                for m in measurements:
                    sensor_type = m.sensor.type
                    if sensor_type not in sensor_measurements:
                        sensor_measurements[sensor_type] = 0
                    sensor_measurements[sensor_type] += 1
                
                print(f"   Measurements by Sensor Type:")
                for sensor_type, count in sorted(sensor_measurements.items()):
                    print(f"     • {sensor_type}: {count:,}")
            
            # Check health logs
            health_logs = StationHealthLog.objects.filter(station=station)
            print(f"   Health Logs: {health_logs.count()}")
            
            if health_logs.exists():
                latest_health = health_logs.order_by('-created_at').first()
                print(f"   Latest Health: {latest_health.created_at}")
                print(f"   Battery: {latest_health.battery_status}")
                print(f"   Connectivity: {latest_health.connectivity_status}")
    
    print(f"\n=== COMPARISON WITH 3D_PAWS STATIONS ===")
    
    # Get 3D_Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    paws_stations = Station.objects.filter(brand=paws_brand).exclude(status='Decommissioned')
    
    print(f"3D_Paws stations ({paws_stations.count()} total):")
    
    # Look for patterns in 3D_Paws stations
    paws_patterns = []
    for station in paws_stations:
        if station.name.startswith('T'):
            paws_patterns.append(station.name)
    
    print(f"3D_Paws stations with 'T' prefix: {len(paws_patterns)}")
    for pattern in sorted(paws_patterns):
        print(f"  • {pattern}")
    
    print(f"\n=== COMPARISON WITH OTT STATIONS ===")
    
    # Get OTT brand
    ott_brand = Brand.objects.get(name='OTT')
    ott_stations = Station.objects.filter(brand=ott_brand).exclude(status='Decommissioned')
    
    print(f"OTT stations ({ott_stations.count()} total):")
    
    # Look for patterns in OTT stations
    ott_patterns = []
    for station in ott_stations:
        if station.name.startswith('T'):
            ott_patterns.append(station.name)
    
    print(f"OTT stations with 'T' prefix: {len(ott_patterns)}")
    for pattern in sorted(ott_patterns):
        print(f"  • {pattern}")
    
    print(f"\n=== SENSOR BRAND ANALYSIS ===")
    
    # Check what sensor brands are used by each station type
    for station_name in station_names:
        station = Station.objects.filter(name=station_name).first()
        if station:
            print(f"\n{station.name} sensors:")
            station_sensors = StationSensor.objects.filter(station=station)
            
            sensor_brands = {}
            for ss in station_sensors:
                sensor = ss.sensor
                brand_name = sensor.brand.name if sensor.brand else 'No Brand'
                if brand_name not in sensor_brands:
                    sensor_brands[brand_name] = []
                sensor_brands[brand_name].append(sensor.type)
            
            for brand_name, sensor_types in sensor_brands.items():
                print(f"  {brand_name}: {', '.join(sensor_types)}")
    
    print(f"\n=== MEASUREMENT PATTERNS ===")
    
    # Check if these stations have similar measurement patterns to 3D_Paws or OTT
    for station_name in station_names:
        station = Station.objects.filter(name=station_name).first()
        if station:
            print(f"\n{station.name} measurement analysis:")
            
            # Get recent measurements (last 7 days)
            one_week_ago = timezone.now() - timedelta(days=7)
            recent_measurements = Measurement.objects.filter(
                station=station,
                created_at__gte=one_week_ago
            )
            
            print(f"  Recent measurements (7 days): {recent_measurements.count()}")
            
            if recent_measurements.exists():
                # Check measurement frequency
                measurement_dates = recent_measurements.values_list('created_at', flat=True).distinct()
                print(f"  Days with data: {len(measurement_dates)}")
                
                # Check sensor types with recent data
                recent_sensor_types = recent_measurements.values_list('sensor__type', flat=True).distinct()
                print(f"  Active sensor types: {', '.join(recent_sensor_types)}")
    
    print(f"\n=== RECOMMENDATION ANALYSIS ===")
    
    # Analyze if these stations should be moved to 3D_Paws
    print("Based on the analysis above, here are the key factors to consider:")
    print("1. Station naming patterns (T prefix)")
    print("2. Sensor brand assignments")
    print("3. Measurement patterns and frequency")
    print("4. Geographic location and purpose")
    print("5. Historical data consistency")
    
    print(f"\nTo determine if these stations should be moved to 3D_Paws, check:")
    print("- Do they use 3D_Paws brand sensors?")
    print("- Do they follow 3D_Paws measurement patterns?")
    print("- Are they geographically grouped with other 3D_Paws stations?")
    print("- Do they have similar data quality and frequency?")

if __name__ == "__main__":
    investigate_t14_t15_t16() 