#!/usr/bin/env python
"""
Check database table structure and column names
Run with: python check_db_structure.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

def check_db_structure():
    print("=== DATABASE STRUCTURE CHECK ===\n")
    
    with connection.cursor() as cursor:
        # Check if we're using MySQL or SQLite
        try:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            db_type = "MySQL"
            print(f"Database type: {db_type}")
            print(f"MySQL version: {version}")
        except:
            db_type = "PostgreSQL"
            print(f"Database type: {db_type}")
        
        # Get all table names
        if db_type == "SQLite":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        else:
            cursor.execute("SHOW TABLES")
        
        tables = cursor.fetchall()
        print(f"\nTotal tables: {len(tables)}")
        
        # Check StationSensor table specifically
        print("\n=== STATIONSENSOR TABLE STRUCTURE ===")
        
        if db_type == "SQLite":
            cursor.execute("PRAGMA table_info(station_sensors)")
        else:
            cursor.execute("DESCRIBE station_sensors")
        
        columns = cursor.fetchall()
        print("Station_sensors table columns:")
        for col in columns:
            if db_type == "SQLite":
                print(f"  {col[1]} ({col[2]}) - Primary Key: {col[5]}")
            else:
                print(f"  {col[0]} ({col[1]}) - Key: {col[3]}")
        
        # Check stations table
        print("\n=== STATIONS TABLE STRUCTURE ===")
        
        if db_type == "SQLite":
            cursor.execute("PRAGMA table_info(stations)")
        else:
            cursor.execute("DESCRIBE stations")
        
        station_columns = cursor.fetchall()
        print("Stations table columns:")
        for col in station_columns:
            if db_type == "SQLite":
                print(f"  {col[1]} ({col[2]}) - Primary Key: {col[5]}")
            else:
                print(f"  {col[0]} ({col[1]}) - Key: {col[3]}")
        
        # Check brands table
        print("\n=== BRANDS TABLE STRUCTURE ===")
        
        if db_type == "SQLite":
            cursor.execute("PRAGMA table_info(brands)")
        else:
            cursor.execute("DESCRIBE brands")
        
        brand_columns = cursor.fetchall()
        print("Brands table columns:")
        for col in brand_columns:
            if db_type == "SQLite":
                print(f"  {col[1]} ({col[2]}) - Primary Key: {col[5]}")
            else:
                print(f"  {col[0]} ({col[1]}) - Key: {col[3]}")
        
        # Check measurements table
        print("\n=== MEASUREMENTS TABLE STRUCTURE ===")
        
        if db_type == "SQLite":
            cursor.execute("PRAGMA table_info(measurements)")
        else:
            cursor.execute("DESCRIBE measurements")
        
        measurement_columns = cursor.fetchall()
        print("Measurements table columns:")
        for col in measurement_columns:
            if db_type == "SQLite":
                print(f"  {col[1]} ({col[2]}) - Primary Key: {col[5]}")
            else:
                print(f"  {col[0]} ({col[1]}) - Key: {col[3]}")
        
        # Check current data counts
        print("\n=== CURRENT DATA COUNTS ===")
        
        cursor.execute("SELECT COUNT(*) FROM station_sensors")
        station_sensor_count = cursor.fetchone()[0]
        print(f"Station_sensors: {station_sensor_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM stations")
        stations_count = cursor.fetchone()[0]
        print(f"Stations: {stations_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM brands")
        brands_count = cursor.fetchone()[0]
        print(f"Brands: {brands_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM measurements")
        measurements_count = cursor.fetchone()[0]
        print(f"Measurements: {measurements_count} records")
        
        # Check for any duplicate relationships
        print("\n=== CHECKING FOR DUPLICATES ===")
        
        cursor.execute("""
            SELECT station_id, sensor_id, COUNT(*) as count
            FROM station_sensors 
            GROUP BY station_id, sensor_id 
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """)
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"Found {len(duplicates)} duplicate combinations:")
            for station_id, sensor_id, count in duplicates[:5]:
                print(f"  Station {station_id}, Sensor {sensor_id}: {count} relationships")
            if len(duplicates) > 5:
                print(f"  ... and {len(duplicates) - 5} more")
        else:
            print("No duplicate relationships found")
    
    print("\n=== END OF STRUCTURE CHECK ===")

if __name__ == "__main__":
    check_db_structure() 