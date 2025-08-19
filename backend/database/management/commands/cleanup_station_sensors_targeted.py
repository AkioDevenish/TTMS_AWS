from django.core.management.base import BaseCommand
from database.models import StationSensor, Measurement, Station, Sensor, Brand
from django.db import transaction
from django.db.models import Q


class Command(BaseCommand):
    help = 'Clean up StationSensor relationships for specific brands using efficient queries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--brand',
            type=str,
            choices=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'all'],
            default='all',
            help='Specific brand to clean up (default: all)',
        )
        parser.add_argument(
            '--cleanup-duplicates',
            action='store_true',
            help='Also clean up duplicate relationships',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        brand_filter = options['brand']
        
        if dry_run:
            self.stdout.write('DRY RUN MODE - No changes will be made')
        
        self.stdout.write(f'Targeting brand: {brand_filter}')
        
        # Get the brands we care about
        if brand_filter == 'all':
            target_brands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT']
        else:
            target_brands = [brand_filter]
        
        # Get stations for these brands
        target_stations = Station.objects.filter(brand__name__in=target_brands)
        self.stdout.write(f'Found {target_stations.count()} stations for brands: {target_brands}')
        
        # Get all StationSensor relationships for these stations
        target_relationships = StationSensor.objects.filter(station__in=target_stations)
        total_relationships = target_relationships.count()
        self.stdout.write(f'Total StationSensor relationships for target brands: {total_relationships}')
        
        # Use a more efficient approach - get all station-sensor combinations that have measurements
        # This avoids the N+1 query problem
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT station_id, sensor_id 
                FROM measurements 
                WHERE station_id IN %s
            """, [tuple(target_stations.values_list('id', flat=True))])
            
            valid_combinations = set(cursor.fetchall())
        
        self.stdout.write(f'Valid station-sensor combinations with measurements: {len(valid_combinations)}')
        
        # Find relationships to remove
        relationships_to_remove = []
        
        # Process in batches to avoid memory issues
        batch_size = 1000
        processed = 0
        
        for batch_start in range(0, total_relationships, batch_size):
            batch_end = min(batch_start + batch_size, total_relationships)
            batch_relationships = target_relationships[batch_start:batch_end]
            
            for relationship in batch_relationships:
                # Check if this combination has measurements
                has_measurements = (relationship.station_id, relationship.sensor_id) in valid_combinations
                
                if not has_measurements:
                    relationships_to_remove.append(relationship.id)  # Store just the IDs
            
            processed += len(batch_relationships)
            self.stdout.write(f'Processed {processed}/{total_relationships} relationships...')
        
        self.stdout.write(f'Relationships to remove: {len(relationships_to_remove)}')
        
        if relationships_to_remove:
            if not dry_run:
                with transaction.atomic():
                    # Delete in batches to avoid long transactions
                    delete_batch_size = 1000
                    deleted_count = 0
                    
                    for i in range(0, len(relationships_to_remove), delete_batch_size):
                        batch_ids = relationships_to_remove[i:i + delete_batch_size]
                        deleted_batch = StationSensor.objects.filter(id__in=batch_ids).delete()
                        deleted_count += deleted_batch[0]
                        self.stdout.write(f'Deleted batch {i//delete_batch_size + 1}: {deleted_batch[0]} relationships')
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully removed {deleted_count} StationSensor relationships'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Would remove {len(relationships_to_remove)} StationSensor relationships (dry run)'
                    )
                )
        else:
            self.stdout.write(
                self.style.SUCCESS('No problematic StationSensor relationships found')
            )
        
        # Show final counts
        final_count = StationSensor.objects.filter(station__in=target_stations).count()
        self.stdout.write(f'Final StationSensor relationships for target brands: {final_count}')
        
        # Show some statistics
        for brand_name in target_brands:
            brand_stations = Station.objects.filter(brand__name=brand_name)
            brand_relationships = StationSensor.objects.filter(station__in=brand_stations).count()
            brand_measurements = Measurement.objects.filter(station__in=brand_stations).count()
            
            self.stdout.write(f'{brand_name}: {brand_stations.count()} stations, {brand_relationships} relationships, {brand_measurements} measurements')
        
        # Clean up duplicates if requested
        if options.get('cleanup_duplicates'):
            self.stdout.write('\n=== Cleaning up duplicate relationships ===')
            self.cleanup_duplicate_relationships(dry_run=dry_run)
    
    def cleanup_duplicate_relationships(self, dry_run=True):
        """Clean up duplicate StationSensor relationships for the same station-sensor combination"""
        if dry_run:
            self.stdout.write('DRY RUN MODE - No changes will be made')
        
        self.stdout.write('Looking for duplicate StationSensor relationships...')
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Find duplicate relationships
            cursor.execute("""
                SELECT station_id, sensor_id, COUNT(*) as count
                FROM station_sensors 
                GROUP BY station_id, sensor_id 
                HAVING COUNT(*) > 1
                ORDER BY count DESC
            """)
            
            duplicates = cursor.fetchall()
        
        if not duplicates:
            self.stdout.write(self.style.SUCCESS('No duplicate relationships found'))
            return
        
        self.stdout.write(f'Found {len(duplicates)} duplicate relationship groups:')
        
        total_duplicates = 0
        for station_id, sensor_id, count in duplicates[:10]:  # Show first 10
            self.stdout.write(f'  Station {station_id}, Sensor {sensor_id}: {count} relationships')
            total_duplicates += (count - 1)  # Keep 1, remove the rest
        
        if len(duplicates) > 10:
            self.stdout.write(f'  ... and {len(duplicates) - 10} more groups')
        
        self.stdout.write(f'Total duplicate relationships to remove: {total_duplicates}')
        
        if not dry_run and total_duplicates > 0:
            with transaction.atomic():
                # Remove duplicates, keeping only the first one
                cursor.execute("""
                    DELETE FROM station_sensors 
                    WHERE id NOT IN (
                        SELECT MIN(id) 
                        FROM station_sensors 
                        GROUP BY station_id, sensor_id
                    )
                """)
                
                deleted_count = cursor.rowcount
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully removed {deleted_count} duplicate relationships'
                    )
                )
        elif dry_run and total_duplicates > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'Would remove {total_duplicates} duplicate relationships (dry run)'
                )
            ) 