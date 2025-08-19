from django.core.management.base import BaseCommand
from database.models import Station, Brand

class Command(BaseCommand):
    help = 'Check station data and brand assignments'

    def handle(self, *args, **options):
        self.stdout.write("Checking station data...")
        
        # Get all brands
        brands = Brand.objects.all()
        self.stdout.write(f"Total brands: {brands.count()}")
        for brand in brands:
            self.stdout.write(f"  - {brand.id}: {brand.name}")
        
        # Get all stations
        stations = Station.objects.select_related('brand').all()
        self.stdout.write(f"\nTotal stations: {stations.count()}")
        
        # Group stations by brand
        stations_by_brand = {}
        for station in stations:
            brand_name = station.brand.name if station.brand else 'No Brand'
            if brand_name not in stations_by_brand:
                stations_by_brand[brand_name] = []
            stations_by_brand[brand_name].append(station)
        
        # Display stations by brand
        for brand_name, station_list in stations_by_brand.items():
            self.stdout.write(f"\n{brand_name} ({len(station_list)} stations):")
            for station in station_list[:10]:  # Show first 10 stations
                self.stdout.write(f"  - {station.name} (ID: {station.id})")
            if len(station_list) > 10:
                self.stdout.write(f"  ... and {len(station_list) - 10} more")
        
        # Check for stations with "POSSAT" in the name
        possat_stations = stations.filter(name__icontains='POSSAT')
        if possat_stations.exists():
            self.stdout.write(f"\nPOSSAT stations found ({possat_stations.count()}):")
            for station in possat_stations:
                self.stdout.write(f"  - {station.name} (ID: {station.id}) -> Brand: {station.brand.name if station.brand else 'No Brand'}")
        else:
            self.stdout.write("\nNo stations with 'POSSAT' in the name found.")
        
        # Check for stations with "Rawinsonde" in the name
        rawinsonde_stations = stations.filter(name__icontains='Rawinsonde')
        if rawinsonde_stations.exists():
            self.stdout.write(f"\nRawinsonde stations found ({rawinsonde_stations.count()}):")
            for station in rawinsonde_stations:
                self.stdout.write(f"  - {station.name} (ID: {station.id}) -> Brand: {station.brand.name if station.brand else 'No Brand'}")
        else:
            self.stdout.write("\nNo stations with 'Rawinsonde' in the name found.") 