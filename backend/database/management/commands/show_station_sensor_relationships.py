from django.core.management.base import BaseCommand
from database.models import Brand, Station, Sensor, StationSensor
from django.db.models import Count, Q


class Command(BaseCommand):
    help = 'Display station-sensor relationships for specific brands'

    def add_arguments(self, parser):
        parser.add_argument(
            '--brands',
            nargs='+',
            type=str,
            default=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT'],
            help='Show relationships for specific brands (default: 3D_Paws, Allmeteo, Zentra, OTT)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['detailed', 'summary', 'csv'],
            default='detailed',
            help='Output format: detailed, summary, or csv'
        )
        parser.add_argument(
            '--station-only',
            action='store_true',
            help='Show only stations without sensor details'
        )

    def handle(self, *args, **options):
        brands = options['brands']
        output_format = options['format']
        station_only = options['station_only']
        
        self.stdout.write(self.style.SUCCESS(f"=== Station-Sensor Relationships for Brands: {', '.join(brands)} ===\n"))
        
        # Get the requested brands
        brand_objects = Brand.objects.filter(name__in=brands)
        if not brand_objects.exists():
            self.stdout.write(self.style.ERROR(f"No brands found: {brands}"))
            return
            
        # Show summary first
        self._show_summary(brand_objects)
        
        if output_format == 'summary':
            return
            
        # Show detailed relationships
        for brand in brand_objects:
            self._show_brand_relationships(brand, output_format, station_only)
            
        # Show cross-brand summary
        self._show_cross_brand_summary(brand_objects)

    def _show_summary(self, brand_objects):
        """Show summary statistics for all requested brands"""
        self.stdout.write(self.style.SUCCESS("=== SUMMARY STATISTICS ==="))
        
        total_stations = 0
        total_sensors = 0
        total_relationships = 0
        
        for brand in brand_objects:
            stations_count = Station.objects.filter(brand=brand).count()
            sensors_count = Sensor.objects.filter(brand=brand).count()
            relationships_count = StationSensor.objects.filter(
                Q(station__brand=brand) | Q(sensor__brand=brand)
            ).count()
            
            total_stations += stations_count
            total_sensors += sensors_count
            total_relationships += relationships_count
            
            self.stdout.write(f"\n{brand.name}:")
            self.stdout.write(f"  Stations: {stations_count}")
            self.stdout.write(f"  Sensors: {sensors_count}")
            self.stdout.write(f"  Relationships: {relationships_count}")
        
        self.stdout.write(f"\nTOTAL:")
        self.stdout.write(f"  Stations: {total_stations}")
        self.stdout.write(f"  Sensors: {total_sensors}")
        self.stdout.write(f"  Relationships: {total_relationships}")
        self.stdout.write("")

    def _show_brand_relationships(self, brand, output_format, station_only):
        """Show detailed relationships for a specific brand"""
        self.stdout.write(self.style.SUCCESS(f"\n=== {brand.name.upper()} ==="))
        self.stdout.write("=" * (len(brand.name) + 4))
        
        # Get stations for this brand
        stations = Station.objects.filter(brand=brand).prefetch_related(
            'station_sensors__sensor'
        ).order_by('name')
        
        if not stations.exists():
            self.stdout.write(f"No stations found for {brand.name}")
            return
            
        if output_format == 'csv':
            self._output_csv(brand, stations, station_only)
        else:
            self._output_detailed(brand, stations, station_only)

    def _output_detailed(self, brand, stations, station_only):
        """Output detailed relationships in readable format"""
        for station in stations:
            self.stdout.write(f"\n📍 {station.name} (SN: {station.serial_number})")
            self.stdout.write(f"   Status: {station.status}")
            self.stdout.write(f"   Location: {station.address}")
            if station.latitude and station.longitude:
                self.stdout.write(f"   Coordinates: {station.latitude}, {station.longitude}")
            
            if not station_only:
                station_sensors = station.station_sensors.all()
                if station_sensors.exists():
                    self.stdout.write(f"   Sensors ({station_sensors.count()}):")
                    for ss in station_sensors:
                        sensor = ss.sensor
                        sensor_brand = f" [{sensor.brand.name}]" if sensor.brand else ""
                        self.stdout.write(f"     • {sensor.type} ({sensor.unit}){sensor_brand}")
                else:
                    self.stdout.write("   Sensors: None configured")

    def _output_csv(self, brand, stations, station_only):
        """Output relationships in CSV format"""
        if not station_only:
            # CSV header
            self.stdout.write("Station,SerialNumber,Status,Address,Latitude,Longitude,SensorType,SensorUnit,SensorBrand")
            
            for station in stations:
                station_sensors = station.station_sensors.all()
                if station_sensors.exists():
                    for ss in station_sensors:
                        sensor = ss.sensor
                        sensor_brand = sensor.brand.name if sensor.brand else "Unknown"
                        self.stdout.write(
                            f'"{station.name}","{station.serial_number}","{station.status}","{station.address}",'
                            f'{station.latitude or ""},{station.longitude or ""},'
                            f'"{sensor.type}","{sensor.unit}","{sensor_brand}"'
                        )
                else:
                    # Station with no sensors
                    self.stdout.write(
                        f'"{station.name}","{station.serial_number}","{station.status}","{station.address}",'
                        f'{station.latitude or ""},{station.longitude or ""},,,'
                    )
        else:
            # CSV header for stations only
            self.stdout.write("Brand,Station,SerialNumber,Status,Address,Latitude,Longitude")
            for station in stations:
                self.stdout.write(
                    f'"{brand.name}","{station.name}","{station.serial_number}","{station.status}","{station.address}",'
                    f'{station.latitude or ""},{station.longitude or ""}'
                )

    def _show_cross_brand_summary(self, brand_objects):
        """Show cross-brand analysis"""
        self.stdout.write(self.style.SUCCESS("\n=== CROSS-BRAND ANALYSIS ==="))
        
        # Find sensors that are used across multiple brands
        cross_brand_sensors = StationSensor.objects.values('sensor__type').annotate(
            brand_count=Count('station__brand', distinct=True)
        ).filter(brand_count__gt=1)
        
        if cross_brand_sensors.exists():
            self.stdout.write("\nSensors used across multiple brands:")
            for sensor_info in cross_brand_sensors:
                sensor_type = sensor_info['sensor__type']
                brand_count = sensor_info['brand_count']
                self.stdout.write(f"  • {sensor_type}: {brand_count} brands")
        
        # Find stations with sensors from different brands
        mixed_brand_stations = Station.objects.filter(
            brand__in=brand_objects
        ).annotate(
            sensor_brand_count=Count('station_sensors__sensor__brand', distinct=True)
        ).filter(sensor_brand_count__gt=1)
        
        if mixed_brand_stations.exists():
            self.stdout.write(f"\nStations with sensors from multiple brands: {mixed_brand_stations.count()}")
            for station in mixed_brand_stations[:5]:  # Show first 5
                self.stdout.write(f"  • {station.name} ({station.sensor_brand_count} sensor brands)") 