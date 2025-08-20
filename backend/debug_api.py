#!/usr/bin/env python
"""
Debug script to test the API endpoints and see what data is being returned
Run with: python debug_api.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import RequestFactory
from database.views import MeasurementViewSet
from database.models import Station, Measurement, StationSensor, Sensor

def test_station_overview():
    print("=== TESTING STATION OVERVIEW ENDPOINT ===\n")
    
    # Create a mock request factory
    factory = RequestFactory()
    
    # Test with 3D Paws and bt1 sensor type
    request = factory.get('/api/measurements/station_overview/?brand=3D_Paws&sensor_type=bt1')
    request.user = None  # Mock user
    
    viewset = MeasurementViewSet()
    viewset.request = request
    
    try:
        response = viewset.station_overview(request)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"Response data keys: {list(data.keys())}")
            print(f"Total stations: {data.get('total', 0)}")
            
            stations = data.get('stations', [])
            print(f"Stations returned: {len(stations)}")
            
            for i, station in enumerate(stations[:3]):  # Show first 3
                print(f"\nStation {i+1}: {station['name']}")
                print(f"  ID: {station['id']}")
                print(f"  Brand: {station['brand']}")
                print(f"  Sensor Unit: {station['sensor_unit']}")
                
                if station.get('latest_measurement'):
                    measurement = station['latest_measurement']
                    print(f"  Latest Measurement:")
                    print(f"    Value: {measurement['value']}")
                    print(f"    Date: {measurement['date']}")
                    print(f"    Time: {measurement['time']}")
                    print(f"    Status: {measurement['status']}")
                else:
                    print(f"  No latest measurement")
        else:
            print(f"Error response: {response.data}")
    except Exception as e:
        print(f"Error testing station_overview: {e}")
        import traceback
        traceback.print_exc()

def test_history_endpoint():
    print(f"\n=== TESTING HISTORY ENDPOINT ===\n")
    
    # Create a mock request factory
    factory = RequestFactory()
    
    # Test with station ID 24 and bt1 sensor type
    request = factory.get('/api/measurements/history/?station_ids=24&sensor_type=bt1&hours=12')
    request.user = None  # Mock user
    
    viewset = MeasurementViewSet()
    viewset.request = request
    
    try:
        response = viewset.history(request)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"Response data keys: {list(data.keys())}")
            
            measurements = data.get('measurements', [])
            print(f"Measurements returned: {len(measurements)}")
            
            for i, measurement in enumerate(measurements[:5]):  # Show first 5
                print(f"\nMeasurement {i+1}:")
                print(f"  Station ID: {measurement['station_id']}")
                print(f"  Sensor Type: {measurement['sensor_type']}")
                print(f"  Value: {measurement['value']}")
                print(f"  Date: {measurement['date']}")
                print(f"  Time: {measurement['time']}")
        else:
            print(f"Error response: {response.data}")
    except Exception as e:
        print(f"Error testing history: {e}")
        import traceback
        traceback.print_exc()

def test_database_data():
    print(f"\n=== TESTING DATABASE DATA ===\n")
    
    # Check 3D Paws stations
    print("3D Paws stations:")
    paws_stations = Station.objects.filter(brand__name='3D_Paws')
    print(f"Total 3D Paws stations: {paws_stations.count()}")
    
    for station in paws_stations[:3]:  # Show first 3
        print(f"\nStation: {station.name} (ID: {station.id})")
        
        # Check station sensors
        station_sensors = StationSensor.objects.filter(station=station)
        print(f"  Configured sensors: {station_sensors.count()}")
        
        for ss in station_sensors:
            sensor = ss.sensor
            print(f"    {sensor.type}")
            
            # Check measurements for this sensor
            measurements = Measurement.objects.filter(station=station, sensor=sensor)
            count = measurements.count()
            latest = measurements.order_by('-date', '-time').first()
            
            print(f"      Measurements: {count}")
            if latest:
                print(f"      Latest: {latest.date} {latest.time} - Value: {latest.value}")
    
    # Check bt1 sensor specifically
    print(f"\n=== BT1 SENSOR DATA ===\n")
    bt1_sensors = Sensor.objects.filter(type='bt1')
    print(f"BT1 sensors found: {bt1_sensors.count()}")
    
    for sensor in bt1_sensors:
        print(f"\nBT1 Sensor: {sensor.type} (ID: {sensor.id})")
        
        # Check which stations use this sensor
        station_sensors = StationSensor.objects.filter(sensor=sensor)
        print(f"      Used by {station_sensors.count()} stations:")
        
        for ss in station_sensors:
            station = ss.station
            print(f"        {station.name} (ID: {station.id})")
            
            # Check measurements
            measurements = Measurement.objects.filter(station=station, sensor=sensor)
            count = measurements.count()
            latest = measurements.order_by('-date', '-time').first()
            
            print(f"          Total measurements: {count}")
            if latest:
                print(f"          Latest: {latest.date} {latest.time} - Value: {latest.value}")

def test_sensor_types_with_data():
    print(f"\n=== TESTING SENSOR TYPES WITH DATA ===\n")
    
    # Check what sensor types actually have data for 3D Paws stations
    paws_stations = Station.objects.filter(brand__name='3D_Paws')
    
    for station in paws_stations[:5]:  # Show first 5
        print(f"\nStation: {station.name} (ID: {station.id})")
        
        # Get ALL measurements for this station (no time filter)
        all_measurements = Measurement.objects.filter(
            station=station
        ).select_related('sensor').order_by('sensor__type')
        
        if all_measurements.exists():
            print(f"  ALL measurements (no time filter):")
            
            # Group by sensor type
            sensor_data = {}
            for m in all_measurements:
                sensor_type = m.sensor.type
                if sensor_type not in sensor_data:
                    sensor_data[sensor_type] = []
                sensor_data[sensor_type].append(m)
            
            for sensor_type, measurements in sensor_data.items():
                latest = max(measurements, key=lambda x: (x.date, x.time))
                print(f"    {sensor_type}: {len(measurements)} measurements, latest: {latest.date} {latest.time} - {latest.value}")
        else:
            print(f"  No measurements at all for this station")

if __name__ == "__main__":
    test_station_overview()
    test_history_endpoint()
    test_database_data()
    test_sensor_types_with_data() 