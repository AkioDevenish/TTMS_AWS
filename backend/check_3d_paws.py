#!/usr/bin/env python
"""
Detailed script to check 3D_Paws station relationships and measurements
Run with: python check_3d_paws.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand

def check_3d_paws_details():
    print("=== 3D_PAWS STATION DETAILED CHECK ===\n")
    
    # Get 3D_Paws brand
    paws_brand = Brand.objects.get(name='3D_Paws')
    print(f"3D_Paws Brand ID: {paws_brand.id}")
    
    # Get 3D_Paws stations
    paws_stations = Station.objects.filter(brand=paws_brand)
    print(f"3D_Paws Stations: {paws_stations.count()}")
    
    for station in paws_stations:
        print(f"\n--- Station: {station.name} (ID: {station.id}) ---")
        
        # Get all relationships for this station
        relationships = StationSensor.objects.filter(station=station)
        print(f"  Total relationships: {relationships.count()}")
        
        # Group by sensor type
        sensor_counts = {}
        for rel in relationships:
            sensor_type = rel.sensor.type
            if sensor_type not in sensor_counts:
                sensor_counts[sensor_type] = 0
            sensor_counts[sensor_type] += 1
        
        print("  Relationships by sensor type:")
        for sensor_type, count in sorted(sensor_counts.items()):
            print(f"    {sensor_type}: {count} relationships")
        
        # Check measurements
        measurements = Measurement.objects.filter(station=station)
        print(f"  Total measurements: {measurements.count()}")
        
        # Check if measurements exist for each sensor type
        print("  Sensors with measurements:")
        for sensor_type in sensor_counts.keys():
            sensor_measurements = Measurement.objects.filter(
                station=station,
                sensor__type=sensor_type
            ).count()
            print(f"    {sensor_type}: {sensor_measurements} measurements")
    
    print("\n=== SUMMARY ===")
    
    # Check total 3D_Paws relationships vs measurements
    total_relationships = StationSensor.objects.filter(station__brand=paws_brand).count()
    total_measurements = Measurement.objects.filter(station__brand=paws_brand).count()
    
    print(f"Total 3D_Paws StationSensor relationships: {total_relationships}")
    print(f"Total 3D_Paws measurements: {total_measurements}")
    
    # Check specific sensor types that should have data
    common_sensors = ['bt1', 'mt1', 'bp1', 'ws', 'wd', 'rg', 'sv1', 'si1', 'su1', 'bpc', 'css']
    
    print("\n=== CHECKING COMMON 3D_PAWS SENSORS ===")
    for sensor_type in common_sensors:
        # Check if this sensor type exists in the database
        sensors = Sensor.objects.filter(type=sensor_type)
        if sensors.exists():
            print(f"\nSensor type '{sensor_type}':")
            print(f"  Total sensors in database: {sensors.count()}")
            
            # Check how many stations have this sensor
            station_sensors = StationSensor.objects.filter(
                sensor__type=sensor_type,
                station__brand=paws_brand
            )
            print(f"  Stations with this sensor: {station_sensors.count()}")
            
            # Check measurements for this sensor type
            measurements = Measurement.objects.filter(
                sensor__type=sensor_type,
                station__brand=paws_brand
            )
            print(f"  Total measurements: {measurements.count()}")
            
            if measurements.exists():
                # Show some sample measurements
                sample_measurements = measurements[:3]
                print(f"  Sample measurements:")
                for m in sample_measurements:
                    print(f"    Station {m.station.name}: {m.value} at {m.date} {m.time}")
        else:
            print(f"\nSensor type '{sensor_type}': NOT FOUND in database")
    
    print("\n=== END OF 3D_PAWS CHECK ===")

if __name__ == "__main__":
    check_3d_paws_details() 