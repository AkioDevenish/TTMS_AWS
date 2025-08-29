#!/usr/bin/env python
"""
Consolidate multiple StationSensor relationships for the same sensor type
Run with: python consolidate_relationships.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Sensor, StationSensor, Measurement, Brand
from django.db import transaction

def consolidate_relationships():
    print("=== CONSOLIDATING STATIONSENSOR RELATIONSHIPS ===\n")
    
    # Check OTT brand specifically
    ott_brand = Brand.objects.get(name='OTT')
    ott_stations = Station.objects.filter(brand=ott_brand)
    
    print("OTT Stations:")
    for station in ott_stations:
        print(f"  {station.name} (ID: {station.id})")
    
    print("\nAnalyzing relationships...")
    
    total_consolidated = 0
    
    for station in ott_stations:
        print(f"\n--- Processing {station.name} ---")
        
        # Get all relationships for this station
        relationships = StationSensor.objects.filter(station=station)
        
        # Group by sensor type
        sensor_groups = {}
        for rel in relationships:
            sensor_type = rel.sensor.type
            if sensor_type not in sensor_groups:
                sensor_groups[sensor_type] = []
            sensor_groups[sensor_type].append(rel)
        
        # Consolidate each sensor type
        for sensor_type, rels in sensor_groups.items():
            if len(rels) > 1:
                print(f"  {sensor_type}: {len(rels)} relationships -> consolidating to 1")
                
                # Keep the first relationship, remove the rest
                keep_rel = rels[0]
                remove_rels = rels[1:]
                
                # Check if any measurements reference the relationships we're about to remove
                for rel in remove_rels:
                    measurements = Measurement.objects.filter(
                        station=station,
                        sensor=rel.sensor
                    )
                    
                    if measurements.exists():
                        # Update measurements to reference the kept relationship
                        measurements.update(sensor=keep_rel.sensor)
                        print(f"    Updated {measurements.count()} measurements to use relationship {keep_rel.id}")
                
                # Remove the extra relationships
                for rel in remove_rels:
                    rel.delete()
                
                total_consolidated += len(remove_rels)
                print(f"    Removed {len(remove_rels)} duplicate relationships")
            else:
                print(f"  {sensor_type}: 1 relationship (no consolidation needed)")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total relationships consolidated: {total_consolidated}")
    
    # Show final state
    final_total = StationSensor.objects.filter(station__brand=ott_brand).count()
    print(f"Final OTT relationships: {final_total}")
    
    print("\n=== END OF CONSOLIDATION ===")

if __name__ == "__main__":
    consolidate_relationships() 