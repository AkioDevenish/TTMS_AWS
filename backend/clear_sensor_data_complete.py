#!/usr/bin/env python
"""
Comprehensive script to clear sensor data while handling foreign key constraints
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection
from django.db import transaction

def clear_sensor_data_complete():
    """Clear sensor data while handling foreign key constraints"""
    
    with connection.cursor() as cursor:
        print("🔍 Analyzing sensor data and dependencies...")
        
        # Check current row counts
        cursor.execute("SELECT COUNT(*) FROM sensors")
        sensors_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM station_sensors")
        station_sensors_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM measurements")
        measurements_count = cursor.fetchone()[0]
        
        print(f"📊 Current data counts:")
        print(f"  - sensors table: {sensors_count} rows")
        print(f"  - station_sensors table: {station_sensors_count} rows")
        print(f"  - measurements table: {measurements_count} rows")
        
        if sensors_count == 0 and station_sensors_count == 0 and measurements_count == 0:
            print("\n✅ All sensor-related tables are already empty!")
            return
        
        # Check foreign key relationships
        print(f"\n🔗 Foreign key relationships:")
        cursor.execute("""
            SELECT 
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE REFERENCED_TABLE_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IN ('sensors', 'station_sensors')
            ORDER BY TABLE_NAME, COLUMN_NAME
        """)
        
        fk_relationships = cursor.fetchall()
        if fk_relationships:
            print("  Tables that reference sensor data:")
            for rel in fk_relationships:
                print(f"    - {rel[0]}.{rel[1]} -> {rel[2]}.{rel[3]}")
        else:
            print("  No foreign key constraints found")
        
        # Ask for confirmation
        total_rows = sensors_count + station_sensors_count + measurements_count
        response = input(f"\n⚠️  Do you want to delete {total_rows} rows from ALL sensor-related tables? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Data deletion cancelled")
            return
        
        print("\n🧹 Starting comprehensive data deletion...")
        
        with transaction.atomic():
            try:
                # Clear in correct order to handle foreign key constraints
                
                # 1. Clear measurements first (references sensors)
                if measurements_count > 0:
                    print(f"  Clearing measurements table ({measurements_count} rows)...")
                    cursor.execute("DELETE FROM measurements")
                    print(f"    ✅ Cleared measurements table")
                
                # 2. Clear station_sensors
                if station_sensors_count > 0:
                    print(f"  Clearing station_sensors table ({station_sensors_count} rows)...")
                    cursor.execute("DELETE FROM station_sensors")
                    print(f"    ✅ Cleared station_sensors table")
                
                # 3. Clear sensors (now safe to do)
                if sensors_count > 0:
                    print(f"  Clearing sensors table ({sensors_count} rows)...")
                    cursor.execute("DELETE FROM sensors")
                    print(f"    ✅ Cleared sensors table")
                
            except Exception as e:
                print(f"    ❌ Error clearing data: {e}")
                return
        
        print("\n✅ Comprehensive data deletion completed!")
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM sensors")
        new_sensors_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM station_sensors")
        new_station_sensors_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM measurements")
        new_measurements_count = cursor.fetchone()[0]
        
        print(f"\n📊 Verification:")
        print(f"  - sensors table: {new_sensors_count} rows (was {sensors_count})")
        print(f"  - station_sensors table: {new_station_sensors_count} rows (was {station_sensors_count})")
        print(f"  - measurements table: {new_measurements_count} rows (was {measurements_count})")
        
        if new_sensors_count == 0 and new_station_sensors_count == 0 and new_measurements_count == 0:
            print("\n🎉 All sensor-related data has been successfully cleared!")
        else:
            print("\n⚠️  Some data may still remain - check manually if needed")

if __name__ == '__main__':
    print("🚀 Comprehensive Sensor Data Clearing Tool")
    print("=" * 55)
    clear_sensor_data_complete() 