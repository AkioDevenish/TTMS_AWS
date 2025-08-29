#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Sensor, Brand
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fix sensors with NULL brand_id by assigning them to correct brands'

    def handle(self, *args, **options):
        # Get all brands
        allmeteo = Brand.objects.get(name='Allmeteo')
        sutron = Brand.objects.get(name='Sutron')
        ott = Brand.objects.get(name='OTT')
        paws_3d = Brand.objects.get(name='3D_Paws')
        zentra = Brand.objects.get(name='Zentra')
        
        # Define sensor type to brand mappings based on usage patterns
        sensor_brand_mappings = {
            # Allmeteo sensors (from logs - these are used by Allmeteo stations)
            'wind_ave10': allmeteo,
            'wind_max10': allmeteo,
            'wind_min10': allmeteo,
            'dir_ave10': allmeteo,
            'dir_max10': allmeteo,
            'dir_lo10': allmeteo,
            'temperature_max': allmeteo,
            'temperature_min': allmeteo,
            'rain_intensity_max': allmeteo,
            'Precipitation': allmeteo,
            'humidity': allmeteo,
            'irradiation': allmeteo,
            'irr_max': allmeteo,
            'pressure': allmeteo,
            'rain_counter': allmeteo,
            
            # 3D_Paws sensors (from data fetcher logic)
            'bpc': paws_3d,  # Battery percentage
            'rg': paws_3d,   # Rain gauge
            'bp1': paws_3d,  # Barometric pressure
            'sv1': paws_3d,  # Solar voltage
            'sil': paws_3d,  # Solar intensity
            'su1': paws_3d,  # Solar UV
            
            # OTT sensors (from existing assignments)
            'Solar Radiation': ott,
            'EvapoTranspiration': ott,
            '5 min rain': ott,
            'Barometric Pressure': ott,
            'Baro Tendency': ott,
            'Daily Rain': ott,
            'Gust Direction': ott,
            'Gust Speed': ott,
            'Hours of Sunshine': ott,
            'Solar Radiation Avg': ott,
            'Solar Radiation Total': ott,
            'Wind Dir Average': ott,
            'Wind Dir Inst': ott,
            'Wind Speed Average': ott,
            'Wind Speed Inst': ott,
            'Battery': ott,
            
            # Zentra sensors (from data fetcher logic)
            'wind_ave10': zentra,  # Wind average
            'wind_max10': zentra,  # Wind maximum
            'wind_min10': zentra,  # Wind minimum
            'dir_ave10': zentra,   # Direction average
            'dir_max10': zentra,   # Direction maximum
            'dir_lo10': zentra,    # Direction low
            'temperature_max': zentra,  # Temperature maximum
            'temperature_min': zentra,  # Temperature minimum
            'rain_intensity_max': zentra,  # Rain intensity
            'Precipitation': zentra,  # Precipitation
            'humidity': zentra,  # Humidity
            'irradiation': zentra,  # Irradiation
            'irr_max': zentra,  # Irradiation maximum
            'pressure': zentra,  # Pressure
            'rain_counter': zentra,  # Rain counter
            
            # Additional sensors that need brand assignment
            'Lightning Activity': allmeteo,  # Lightning detection (Allmeteo MeteoHelix)
            'Lightning Distance': allmeteo,  # Lightning distance (Allmeteo MeteoHelix)
            'Wind Direction': allmeteo,     # Generic wind direction (Allmeteo)
            'Wind Speed': allmeteo,         # Generic wind speed (Allmeteo)
            'Atmospheric Pressure': allmeteo,  # Atmospheric pressure (Allmeteo)
            'X-axis Level': allmeteo,       # Tilt sensor X-axis (Allmeteo)
            'Y-axis Level': allmeteo,       # Tilt sensor Y-axis (Allmeteo)
            'Max Precipitation Rate': allmeteo,  # Max precipitation rate (Allmeteo)
            'RH Sensor Temperature': allmeteo,   # RH sensor temperature (Allmeteo)
            'Vapor Pressure Deficit': allmeteo,  # Vapor pressure deficit (Allmeteo)
            'Reference Pressure': allmeteo,      # Reference pressure (Allmeteo)
        }
        
        # Fix sensors with NULL brand_id
        null_brand_sensors = Sensor.objects.filter(brand__isnull=True)
        fixed_count = 0
        skipped_count = 0
        
        self.stdout.write(f"Found {null_brand_sensors.count()} sensors with NULL brand_id")
        
        for sensor in null_brand_sensors:
            if sensor.type in sensor_brand_mappings:
                sensor.brand = sensor_brand_mappings[sensor.type]
                sensor.save()
                fixed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed: {sensor.type} -> {sensor.brand.name}')
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Skipped: {sensor.type} (no brand mapping found)')
                )
        
        # Show summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'Fix complete: {fixed_count} sensors fixed, {skipped_count} skipped')
        )
        
        # Show remaining NULL sensors
        remaining_null = Sensor.objects.filter(brand__isnull=True)
        if remaining_null.exists():
            self.stdout.write(f'\nRemaining sensors with NULL brand_id ({remaining_null.count()}):')
            for sensor in remaining_null:
                self.stdout.write(f'  - {sensor.type} ({sensor.unit})')
        
        # Show final statistics
        total_sensors = Sensor.objects.count()
        assigned_sensors = Sensor.objects.filter(brand__isnull=False).count()
        self.stdout.write(f'\nFinal statistics:')
        self.stdout.write(f'  Total sensors: {total_sensors}')
        self.stdout.write(f'  Assigned to brands: {assigned_sensors}')
        self.stdout.write(f'  Unassigned: {total_sensors - assigned_sensors}')
        
        # Show sensors by brand
        self.stdout.write(f'\nSensors by brand:')
        for brand in Brand.objects.all():
            count = Sensor.objects.filter(brand=brand).count()
            self.stdout.write(f'  {brand.name}: {count} sensors') 