from django.core.management.base import BaseCommand
from database.models import Sensor, Brand


class Command(BaseCommand):
    help = 'Assign brands to sensors based on data fetcher logic'

    def handle(self, *args, **options):
        # Get all brands
        brands = {brand.name: brand for brand in Brand.objects.all()}
        
        # Define sensor type mappings for each brand
        brand_sensor_mappings = {
            '3D_Paws': [
                'bpc', 'Battery Percent', 'Battery Voltage', 'battery', 'Battery',
                'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct',
                'css', 'sv1', 'si1', 'su1', 'ht1', 'mt1', 'st1', 'bt1', 'ws', 'wd', 'rg', 'bp1', 'sh1', 'bh1', 'hh1',
                'cfr', 'wgd', 'bcs', 'wg', 'hth', 'wbt', 'wbgt', 'hi', 'dir_hi10'
            ],
            'Zentra': [
                'Battery Percent', 'Battery Voltage', 'battery', 'Battery',
                'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct',
                'irradiation', 'irr_max', 'humidity', 'pressure', 'rain_counter', 'temperature'
            ],
            'Allmeteo': [
                'battery', 'Battery', 'Battery Voltage', 'Battery Percent',
                'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct',
                'irradiation', 'irr_max', 'humidity', 'pressure', 'rain_counter', 'temperature'
            ],
            'OTT': [
                'battery', 'Battery', 'Battery Voltage', 'Battery Percent',
                'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct',
                'Solar Radiation', 'Solar Radiation Avg', 'Solar Radiation Total', 'Air Temperature', 'Barometric Pressure',
                'Baro Tendency', 'Daily Rain', '5 min rain', 'Dew Point', 'Gust Direction', 'Gust Speed', 'Hours of Sunshine',
                'Leaf Wetness', 'Maximum Air Temperature', 'Minimum Air Temperature', 'Relative Humidity',
                'Soil Moisture (10cm)', 'Soil Moisture (20cm)', 'Soil Moisture (30cm)', 'Soil Temp (15cm)',
                'Wind Dir Average', 'Wind Dir Inst', 'Wind Speed Average', 'Wind Speed Inst', 'EvapoTranspiration'
            ]
        }
        
        # Track assignments
        assigned_count = 0
        skipped_count = 0
        
        # Process each sensor
        for sensor in Sensor.objects.all():
            assigned = False
            
            # Check each brand's sensor list
            for brand_name, sensor_types in brand_sensor_mappings.items():
                if sensor.type in sensor_types:
                    if brand_name in brands:
                        sensor.brand = brands[brand_name]
                        sensor.save()
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ Assigned {sensor.type} to {brand_name}")
                        )
                        assigned_count += 1
                        assigned = True
                        break
            
            if not assigned:
                self.stdout.write(
                    self.style.WARNING(f"⚠ No brand found for sensor: {sensor.type}")
                )
                skipped_count += 1
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n=== Summary ==="))
        self.stdout.write(self.style.SUCCESS(f"✓ Sensors assigned to brands: {assigned_count}"))
        self.stdout.write(self.style.WARNING(f"⚠ Sensors without brand: {skipped_count}"))
        self.stdout.write(self.style.SUCCESS(f"Total sensors processed: {assigned_count + skipped_count}"))
        
        # Show sensors by brand
        self.stdout.write(self.style.SUCCESS(f"\n=== Sensors by Brand ==="))
        for brand_name in brands:
            brand = brands[brand_name]
            sensors = Sensor.objects.filter(brand=brand)
            if sensors.exists():
                self.stdout.write(f"\n{brand_name}:")
                for sensor in sensors[:10]:  # Show first 10
                    self.stdout.write(f"  - {sensor.type} ({sensor.unit})")
                if sensors.count() > 10:
                    self.stdout.write(f"  ... and {sensors.count() - 10} more") 