#!/usr/bin/env python
"""
Test the fixed sensor matching logic for Allmeteo
Run with: python test_fixed_sensor_matching.py
"""

def test_sensor_matching():
    print("=== TESTING FIXED SENSOR MATCHING LOGIC ===\n")
    
    # Simulate the sensor map from database
    sensor_map = {
        'battery': 37,
        'dewPoint': 47,
        'humidity': 48,
        'irradiation': 49,
        'irradiation_max': 50,
        'pressure': 57,
        'pressure_raw': 51,
        'rain': 52,
        'rainfall_rate_max': 56,
        'temperature': 53,
        'temperature_max': 54,
        'temperature_min': 55,
        'temperature_wetbulb_stull2011_C': 58,
        'wdir_Avg10': 38,
        'wdir_Gust10': 39,
        'wdir_Max10': 40,
        'wdir_Min10': 41,
        'wdir_Stdev10': 46,
        'wind_Avg10': 42,
        'wind_Max10': 43,
        'wind_Min10': 44,
        'wind_Stdev10': 45
    }
    
    # CSV fields from your export
    csv_fields = [
        'battery (V)', 'dewPoint (°C)', 'humidity (%)', 'irradiation (W/m2)',
        'irradiation_max (W/m2)', 'pressure_raw (hPa)', 'rain (mm)', 
        'temperature (°C)', 'temperature_max (°C)', 'temperature_min (°C)',
        'rainfall_rate_max (mm/h)', 'pressure (hPa)', 'temperature_wetbulb_stull2011_C (°C)'
    ]
    
    print("Testing the NEW sensor matching logic:")
    print("1. First try exact match (remove units)")
    print("2. Then try partial match as fallback\n")
    
    for field in csv_fields:
        print(f"Field: {field}")
        
        # NEW LOGIC: First try exact match, then partial match
        matched_sensor = None
        matched_sensor_id = None
        
        # Try exact match first (remove units and special characters)
        clean_field = field.split(' (')[0].strip()  # Remove units like "(V)", "(°C)", etc.
        print(f"  Clean field: '{clean_field}'")
        
        if clean_field in sensor_map:
            matched_sensor = clean_field
            matched_sensor_id = sensor_map[clean_field]
            print(f"  ✅ EXACT MATCH: {matched_sensor} (ID: {matched_sensor_id})")
        else:
            # Try partial match as fallback
            for sensor_type, sensor_id in sensor_map.items():
                if field.lower() in sensor_type.lower() or clean_field.lower() in sensor_type.lower():
                    matched_sensor = sensor_type
                    matched_sensor_id = sensor_id
                    print(f"  ✅ PARTIAL MATCH: {matched_sensor} (ID: {matched_sensor_id})")
                    break
            else:
                print(f"  ❌ NO MATCH FOUND!")
        
        print()

if __name__ == "__main__":
    test_sensor_matching() 