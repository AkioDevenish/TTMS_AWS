from django.core.management.base import BaseCommand
from database.models import StationSensor, Measurement, Station, Sensor
from django.db import transaction


class Command(BaseCommand):
    help = 'Clean up StationSensor relationships that have no actual measurements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write('DRY RUN MODE - No changes will be made')
        
        # Find all StationSensor relationships
        all_relationships = StationSensor.objects.all()
        self.stdout.write(f'Total StationSensor relationships: {all_relationships.count()}')
        
        # Find relationships that have no measurements
        relationships_to_remove = []
        
        for relationship in all_relationships:
            has_measurements = Measurement.objects.filter(
                station=relationship.station,
                sensor=relationship.sensor
            ).exists()
            
            if not has_measurements:
                relationships_to_remove.append(relationship)
        
        self.stdout.write(f'Relationships with no measurements: {len(relationships_to_remove)}')
        
        if relationships_to_remove:
            self.stdout.write('Sample relationships to be removed:')
            for i, rel in enumerate(relationships_to_remove[:10]):
                self.stdout.write(f'  {i+1}. Station: {rel.station.name}, Sensor: {rel.sensor.type}')
            
            if len(relationships_to_remove) > 10:
                self.stdout.write(f'  ... and {len(relationships_to_remove) - 10} more')
            
            if not dry_run:
                with transaction.atomic():
                    # Delete the problematic relationships
                    deleted_count = len(relationships_to_remove)
                    for relationship in relationships_to_remove:
                        relationship.delete()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully removed {deleted_count} StationSensor relationships with no measurements'
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
        final_count = StationSensor.objects.count()
        self.stdout.write(f'Final StationSensor relationships: {final_count}')
        
        # Show some statistics
        stations_count = Station.objects.count()
        sensors_count = Sensor.objects.count()
        measurements_count = Measurement.objects.count()
        
        self.stdout.write(f'Total stations: {stations_count}')
        self.stdout.write(f'Total sensors: {sensors_count}')
        self.stdout.write(f'Total measurements: {measurements_count}')
        
        if measurements_count > 0:
            avg_measurements_per_station = measurements_count / stations_count
            self.stdout.write(f'Average measurements per station: {avg_measurements_per_station:.1f}') 