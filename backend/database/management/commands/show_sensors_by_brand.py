from django.core.management.base import BaseCommand
from database.models import Sensor, Brand


class Command(BaseCommand):
    help = 'Display sensors organized by brand in a clear format'

    def add_arguments(self, parser):
        parser.add_argument(
            '--brand',
            type=str,
            help='Show only sensors for a specific brand (3D_Paws, Allmeteo, Zentra, OTT)'
        )
        parser.add_argument(
            '--count-only',
            action='store_true',
            help='Show only the count of sensors per brand'
        )

    def handle(self, *args, **options):
        if options['brand']:
            # Show sensors for specific brand
            try:
                brand = Brand.objects.get(name=options['brand'])
                sensors = Sensor.objects.filter(brand=brand).order_by('type')
                
                self.stdout.write(self.style.SUCCESS(f"\n=== Sensors for {brand.name} ==="))
                self.stdout.write(f"Total: {sensors.count()} sensors\n")
                
                for sensor in sensors:
                    self.stdout.write(f"  • {sensor.type} ({sensor.unit})")
                    
            except Brand.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Brand '{options['brand']}' not found"))
                return
                
        elif options['count_only']:
            # Show only counts
            self.stdout.write(self.style.SUCCESS("=== Sensor Count by Brand ==="))
            
            for brand in Brand.objects.all().order_by('name'):
                count = Sensor.objects.filter(brand=brand).count()
                self.stdout.write(f"{brand.name}: {count} sensors")
                
        else:
            # Show full breakdown
            self.stdout.write(self.style.SUCCESS("=== Complete Sensor Breakdown by Brand ===\n"))
            
            for brand in Brand.objects.all().order_by('name'):
                sensors = Sensor.objects.filter(brand=brand).order_by('type')
                if sensors.exists():
                    self.stdout.write(self.style.SUCCESS(f"\n{brand.name} ({sensors.count()} sensors):"))
                    self.stdout.write("─" * (len(brand.name) + 20))
                    
                    # Group sensors by category for better organization
                    categories = {}
                    for sensor in sensors:
                        if 'battery' in sensor.type.lower() or 'batt' in sensor.type.lower():
                            category = 'Battery'
                        elif 'temperature' in sensor.type.lower() or 'temp' in sensor.type.lower():
                            category = 'Temperature'
                        elif 'wind' in sensor.type.lower():
                            category = 'Wind'
                        elif 'rain' in sensor.type.lower() or 'precipitation' in sensor.type.lower():
                            category = 'Rain/Precipitation'
                        elif 'pressure' in sensor.type.lower() or 'baro' in sensor.type.lower():
                            category = 'Pressure'
                        elif 'radiation' in sensor.type.lower() or 'irradiation' in sensor.type.lower():
                            category = 'Solar Radiation'
                        elif 'humidity' in sensor.type.lower():
                            category = 'Humidity'
                        elif 'soil' in sensor.type.lower():
                            category = 'Soil'
                        else:
                            category = 'Other'
                        
                        if category not in categories:
                            categories[category] = []
                        categories[category].append(sensor)
                    
                    # Display by category
                    for category in sorted(categories.keys()):
                        if categories[category]:
                            self.stdout.write(f"\n  {category}:")
                            for sensor in categories[category]:
                                self.stdout.write(f"    • {sensor.type} ({sensor.unit})")
            
            # Show unassigned sensors
            unassigned = Sensor.objects.filter(brand__isnull=True)
            if unassigned.exists():
                self.stdout.write(self.style.WARNING(f"\n⚠ Unassigned Sensors ({unassigned.count()}):"))
                self.stdout.write("─" * 30)
                for sensor in unassigned.order_by('type'):
                    self.stdout.write(f"  • {sensor.type} ({sensor.unit})")
            
            # Summary
            total = Sensor.objects.count()
            assigned = Sensor.objects.filter(brand__isnull=False).count()
            self.stdout.write(self.style.SUCCESS(f"\n=== Summary ==="))
            self.stdout.write(f"Total sensors: {total}")
            self.stdout.write(f"Assigned to brands: {assigned}")
            self.stdout.write(f"Unassigned: {total - assigned}") 