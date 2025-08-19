from django.core.management.base import BaseCommand
from django.utils import timezone
from database.models import Station, StationHealthLog
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Create sample station health logs for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample station health logs...')
        
        # Get all active stations
        stations = Station.objects.filter(status='Active')
        
        if not stations.exists():
            self.stdout.write(self.style.ERROR('No active stations found. Please create stations first.'))
            return
        
        # Sample data for different statuses
        battery_statuses = ['Excellent', 'Good', 'Fair', 'Poor', 'Critical']
        connectivity_statuses = ['Excellent', 'Good', 'Fair', 'Poor', 'No Signal', 'No Data']
        
        # Create health logs for each station
        created_count = 0
        for station in stations:
            # Create multiple health logs over the past 24 hours
            for hours_ago in range(0, 25, 2):  # Every 2 hours for 24 hours
                timestamp = timezone.now() - timedelta(hours=hours_ago)
                
                # Randomly assign statuses
                battery_status = random.choice(battery_statuses)
                connectivity_status = random.choice(connectivity_statuses)
                
                # Create the health log
                health_log = StationHealthLog.objects.create(
                    station=station,
                    battery_status=battery_status,
                    connectivity_status=connectivity_status,
                    created_at=timestamp
                )
                created_count += 1
                
                self.stdout.write(f'Created health log for {station.name}: {battery_status} battery, {connectivity_status} connectivity at {timestamp}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample health logs for {stations.count()} stations')
        ) 