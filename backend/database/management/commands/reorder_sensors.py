#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Sensor, Brand
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Reorder sensors in the database by brand and logical categories'

    def handle(self, *args, **options):
        self.stdout.write("Starting sensor reordering...")
        
        try:
            with transaction.atomic():
                # Get all brands in desired order
                brands = Brand.objects.filter(name__in=['3D_Paws', 'OTT', 'Zentra', 'Allmeteo', 'Sutron'])
                
                # Start with ID 1
                current_id = 1
                reordered_sensors = []
                
                for brand in brands:
                    self.stdout.write(f"\nProcessing {brand.name} sensors...")
                    
                    # Get sensors for this brand
                    brand_sensors = Sensor.objects.filter(brand=brand).order_by('type')
                    
                    if brand_sensors.exists():
                        for sensor in brand_sensors:
                            reordered_sensors.append({
                                'id': current_id,
                                'sensor': sensor,
                                'brand_name': brand.name
                            })
                            current_id += 1
                            self.stdout.write(f"  {sensor.type} -> ID {current_id-1}")
                
                # Update sensor IDs to reflect the new order
                self.stdout.write("\nUpdating sensor IDs...")
                for item in reordered_sensors:
                    sensor = item['sensor']
                    new_id = item['id']
                    
                    # Update the sensor ID
                    sensor.id = new_id
                    sensor.save(force_insert=True)
                    
                    self.stdout.write(f"  {sensor.type} ({item['brand_name']}) -> ID {new_id}")
                
                self.stdout.write("\n" + "="*50)
                self.stdout.write(self.style.SUCCESS("Sensor reordering completed successfully!"))
                
                # Show final statistics
                self.stdout.write("\nFinal sensor organization:")
                for brand in brands:
                    count = Sensor.objects.filter(brand=brand).count()
                    if count > 0:
                        self.stdout.write(f"  {brand.name}: {count} sensors")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during reordering: {str(e)}"))
            raise 