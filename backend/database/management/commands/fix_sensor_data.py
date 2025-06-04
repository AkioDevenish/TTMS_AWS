from django.core.management.base import BaseCommand
from database.models import Sensor, Station, StationSensor
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fixes sensor data issues including missing units, duplicate sensors, and inconsistent units'

    def handle(self, *args, **options):
        self.stdout.write('Starting sensor data fixes...')
        
        with transaction.atomic():
            self.fix_missing_units()
            self.consolidate_duplicate_sensors()
            self.standardize_units()
            self.verify_station_sensor_relationships()
        
        self.stdout.write(self.style.SUCCESS('Successfully completed sensor data fixes'))

    def fix_missing_units(self):
        """Add missing units to sensors"""
        self.stdout.write('Fixing missing units...')
        
        # Define unit mappings for sensors without units
        unit_mappings = {
            'Leaf Wetness': '%',
            'Soil Moisture (10cm)': '%',
            'Soil Moisture (20cm)': '%',
            'Soil Moisture (30cm)': '%',
            'Soil Temp (15cm)': '°C',
            '5 min rain': 'mm',
            'Barometric Pressure': 'hPa',
            'Baro Tendency': 'hPa',
            'Battery': 'V',
            'Daily Rain': 'mm',
            'Gust Direction': '°',
            'Gust Speed': 'm/s',
            'Hours of Sunshine': 'hr',
            'Solar Radiation Avg': 'W/m²',
            'Solar Radiation Total': 'W/m²',
            'Wind Dir Average': '°',
            'Wind Dir Inst': '°',
            'Wind Speed Average': 'm/s',
            'Wind Speed Inst': 'm/s',
            'Air Temperature': '°C',
            'Dew Point': '°C',
            'Maximum Air Temperature': '°C',
            'Minimum Air Temperature': '°C',
            'Relative Humidity': '%',
            'EvapoTranspiration': 'mm'
        }

        # Update sensors with missing units
        for sensor_type, unit in unit_mappings.items():
            sensors = Sensor.objects.filter(type=sensor_type, unit='')
            if sensors.exists():
                sensors.update(unit=unit)
                self.stdout.write(f'Updated unit for {sensor_type} to {unit}')

    def consolidate_duplicate_sensors(self):
        """Consolidate duplicate sensor types"""
        self.stdout.write('Consolidating duplicate sensors...')
        
        # Define sensor type mappings (new_type: [old_types])
        sensor_mappings = {
            'Solar Radiation': ['Solar Radiation'],
            'Precipitation': ['Precipitation'],
            'Lightning Activity': ['Lightning Activity'],
            'Lightning Distance': ['Lightning Distance'],
            'Wind Direction': ['Wind Direction'],
            'Wind Speed': ['Wind Speed'],
            'Gust Speed': ['Gust Speed'],
            'Air Temperature': ['Air Temperature'],
            'Relative Humidity': ['Relative Humidity'],
            'Atmospheric Pressure': ['Atmospheric Pressure']
        }

        for new_type, old_types in sensor_mappings.items():
            # Get all sensors of these types
            sensors = Sensor.objects.filter(type__in=old_types)
            if sensors.count() > 1:
                # Get the first sensor as the primary one
                primary_sensor = sensors.first()
                
                # For each duplicate sensor
                for sensor in sensors.exclude(id=primary_sensor.id):
                    # Get all station relationships for this sensor
                    station_relationships = StationSensor.objects.filter(sensor=sensor)
                    
                    for relationship in station_relationships:
                        try:
                            # Try to create relationship with primary sensor if it doesn't exist
                            StationSensor.objects.get_or_create(
                                station=relationship.station,
                                sensor=primary_sensor
                            )
                            # Delete the old relationship
                            relationship.delete()
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f"Could not update relationship for station {relationship.station_id}: {str(e)}"
                            ))
                    
                    # Delete the duplicate sensor
                    sensor.delete()
                
                self.stdout.write(f'Consolidated {sensors.count()} sensors of type {new_type}')

    def standardize_units(self):
        """Standardize units across similar sensors"""
        self.stdout.write('Standardizing units...')
        
        # Define unit standardization mappings
        unit_standardizations = {
            'temperature': {
                'target_unit': '°C',
                'sensors': ['Air Temperature', 'temperature', 'bt1', 'mt1']
            },
            'wind_speed': {
                'target_unit': 'm/s',
                'sensors': ['Wind Speed', 'ws', 'wind_ave10', 'wind_max10', 'wind_min10']
            },
            'pressure': {
                'target_unit': 'hPa',
                'sensors': ['Atmospheric Pressure', 'bp1', 'pressure']
            }
        }

        for category, config in unit_standardizations.items():
            sensors = Sensor.objects.filter(type__in=config['sensors'])
            if sensors.exists():
                sensors.update(unit=config['target_unit'])
                self.stdout.write(f'Standardized {category} units to {config["target_unit"]}')

    def verify_station_sensor_relationships(self):
        """Verify and fix station-sensor relationships"""
        self.stdout.write('Verifying station-sensor relationships...')
        
        # Get all stations and sensors
        stations = Station.objects.all()
        sensors = Sensor.objects.all()
        
        # Create missing relationships
        for station in stations:
            for sensor in sensors:
                StationSensor.objects.get_or_create(
                    station=station,
                    sensor=sensor
                )
        
        self.stdout.write('Verified all station-sensor relationships') 