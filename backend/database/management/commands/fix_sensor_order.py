#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Sensor, Brand
from django.core.management.base import BaseCommand
from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Fix sensor order in database to show them logically grouped by brand and type'

    def handle(self, *args, **options):
        self.stdout.write("Fixing sensor order in database...")
        
        try:
            with transaction.atomic():
                # Get brands in desired order
                brand_order = ['3D_Paws', 'OTT', 'Zentra', 'Allmeteo', 'Sutron']
                brands = {name: Brand.objects.get(name=name) for name in brand_order if Brand.objects.filter(name=name).exists()}
                
                # Create a new table with proper ordering
                with connection.cursor() as cursor:
                    # Instead of recreating the table, let's update the existing IDs
                    # First, let's create a mapping of old IDs to new IDs
                    self.stdout.write("Creating ID mapping...")
                    
                    # Get sensors in the desired order
                    new_id = 1
                    id_mapping = {}  # old_id -> new_id
                    
                    for brand_name in brand_order:
                        if brand_name in brands:
                            brand = brands[brand_name]
                            self.stdout.write(f"\nProcessing {brand_name} sensors...")
                            
                            # Get sensors for this brand, ordered by type
                            brand_sensors = Sensor.objects.filter(brand=brand).order_by('type')
                            
                            for sensor in brand_sensors:
                                id_mapping[sensor.id] = new_id
                                self.stdout.write(f"  Old ID {sensor.id:3d} -> New ID {new_id:3d}: {sensor.type:<25} ({brand_name})")
                                new_id += 1
                    
                    # Now update the IDs in the existing table
                    self.stdout.write(f"\nUpdating sensor IDs in database...")
                    
                    # We need to update IDs carefully to avoid conflicts
                    # First, update to temporary high values
                    for old_id, new_id in id_mapping.items():
                        if old_id != new_id:
                            cursor.execute("UPDATE sensors SET id = %s WHERE id = %s", [new_id + 10000, old_id])
                    
                    # Then update to final values
                    for old_id, new_id in id_mapping.items():
                        if old_id != new_id:
                            cursor.execute("UPDATE sensors SET id = %s WHERE id = %s", [new_id, new_id + 10000])
                    
                    # Reset the auto-increment
                    cursor.execute("ALTER TABLE sensors AUTO_INCREMENT = %s", [new_id])
                
                self.stdout.write(f"\n{self.style.SUCCESS('Sensor reordering completed!')}")
                self.stdout.write(f"Total sensors reordered: {new_id - 1}")
                
                # Verify the new order
                self.stdout.write(f"\nVerifying new order:")
                sensors = Sensor.objects.all().order_by('id')
                for sensor in sensors[:20]:  # Show first 20
                    brand_name = sensor.brand.name if sensor.brand else 'None'
                    self.stdout.write(f"  ID {sensor.id:3d}: {sensor.type:<25} ({brand_name})")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during reordering: {str(e)}"))
            raise 