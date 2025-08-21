#!/usr/bin/env python
"""
Fix station brand assignments - move T14, T15, T16 from OTT to 3D_Paws
Run with: python fix_station_brands.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Station, Brand

def fix_station_brands():
    print("=== FIXING STATION BRAND ASSIGNMENTS ===\n")
    
    # Get the brands
    ott_brand = Brand.objects.get(name='OTT')
    paws_brand = Brand.objects.get(name='3D_Paws')
    
    print(f"OTT Brand ID: {ott_brand.id}")
    print(f"3D_Paws Brand ID: {paws_brand.id}")
    print()
    
    # Stations to fix
    station_names = ['T14 UTT', 'T15 ASJA', 'T16 Lochmaben']
    
    print("=== STATIONS TO BE MOVED ===")
    for station_name in station_names:
        station = Station.objects.filter(name=station_name).first()
        if station:
            print(f"📍 {station.name}")
            print(f"   Current Brand: {station.brand.name}")
            print(f"   Will Move To: 3D_Paws")
            print()
        else:
            print(f"❌ Station '{station_name}' not found!")
            print()
    
    # Confirm the change
    print("=== CONFIRMATION ===")
    print("This will move the following stations from OTT to 3D_Paws brand:")
    for name in station_names:
        print(f"  • {name}")
    
    print(f"\nReason: These stations use 100% 3D_Paws brand sensors")
    print(f"and follow the same naming convention as other 3D_Paws stations.")
    
    # Ask for confirmation
    response = input(f"\nDo you want to proceed? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        print(f"\n=== EXECUTING BRAND CHANGES ===")
        
        stations_moved = 0
        for station_name in station_names:
            station = Station.objects.filter(name=station_name).first()
            if station:
                old_brand = station.brand.name
                station.brand = paws_brand
                station.save()
                stations_moved += 1
                print(f"✅ Moved {station.name} from {old_brand} to 3D_Paws")
            else:
                print(f"❌ Could not find station: {station_name}")
        
        print(f"\n=== SUMMARY ===")
        print(f"Successfully moved {stations_moved} stations to 3D_Paws brand")
        
        # Verify the changes
        print(f"\n=== VERIFICATION ===")
        for station_name in station_names:
            station = Station.objects.filter(name=station_name).first()
            if station:
                print(f"✅ {station.name} is now in {station.brand.name} brand")
            else:
                print(f"❌ {station_name} not found after update")
        
        print(f"\n=== NEXT STEPS ===")
        print(f"1. Restart your Django server if needed")
        print(f"2. Refresh the Station Health dashboard")
        print(f"3. T14, T15, and T16 should now appear in the 3D_Paws tab")
        print(f"4. They should no longer appear in the OTT tab")
        
    else:
        print(f"\n❌ Operation cancelled. No changes were made.")
        print(f"Stations remain in their current brand assignments.")

if __name__ == "__main__":
    fix_station_brands() 