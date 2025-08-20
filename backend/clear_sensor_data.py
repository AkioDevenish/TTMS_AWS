#!/usr/bin/env python
"""
Script to clear data from sensors and station_sensors tables
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection
from django.db import transaction

def clear_sensor_data():
    """Clear data from sensors and station_sensors tables"""
    
    with connection.cursor() as cursor:
        print("🔍 Checking current data in sensor tables...")
        
        # Check current row counts
        cursor.execute("SELECT COUNT(*) FROM sensors")
        sensors_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM station_sensors")
        station_sensors_count = cursor.fetchone()[0]
        
        print(f"📊 Current data counts:")
        print(f"  - sensors table: {sensors_count} rows")
        print(f"  - station_sensors table: {station_sensors_count} rows")
        
        if sensors_count == 0 and station_sensors_count == 0:
            print("\n✅ Both tables are already empty!")
            return
        
        # Ask for confirmation
        total_rows = sensors_count + station_sensors_count
        response = input(f"\n⚠️  Do you want to delete {total_rows} rows from sensor tables? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Data deletion cancelled")
            return
        
        print("\n🧹 Starting data deletion...")
        
        with transaction.atomic():
            try:
                # Clear station_sensors first (due to foreign key constraints)
                if station_sensors_count > 0:
                    print(f"  Clearing station_sensors table ({station_sensors_count} rows)...")
                    cursor.execute("DELETE FROM station_sensors")
                    print(f"    ✅ Cleared station_sensors table")
                
                # Clear sensors table
                if sensors_count > 0:
                    print(f"  Clearing sensors table ({sensors_count} rows)...")
                    cursor.execute("DELETE FROM sensors")
                    print(f"    ✅ Cleared sensors table")
                
            except Exception as e:
                print(f"    ❌ Error clearing data: {e}")
                return
        
        print("\n✅ Data deletion completed!")
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM sensors")
        new_sensors_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM station_sensors")
        new_station_sensors_count = cursor.fetchone()[0]
        
        print(f"\n📊 Verification:")
        print(f"  - sensors table: {new_sensors_count} rows (was {sensors_count})")
        print(f"  - station_sensors table: {new_station_sensors_count} rows (was {station_sensors_count})")
        
        if new_sensors_count == 0 and new_station_sensors_count == 0:
            print("\n🎉 All sensor data has been successfully cleared!")
        else:
            print("\n⚠️  Some data may still remain - check manually if needed")

if __name__ == '__main__':
    print("🚀 Sensor Data Clearing Tool")
    print("=" * 40)
    clear_sensor_data() 