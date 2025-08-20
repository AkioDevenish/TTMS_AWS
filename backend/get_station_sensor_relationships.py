#!/usr/bin/env python
"""
Utility script to fetch station-sensor relationships for specific brands.
This script can be run directly or imported to get data programmatically.
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from database.models import Brand, Station, Sensor, StationSensor
from django.db.models import Count, Q, Prefetch


def get_station_sensor_relationships(brands=None, include_details=True):
    """
    Get station-sensor relationships for specified brands.
    
    Args:
        brands (list): List of brand names to filter by. 
                      Default: ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT']
        include_details (bool): Whether to include full station and sensor details
    
    Returns:
        dict: Dictionary containing the relationships data
    """
    if brands is None:
        brands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT']
    
    # Get the requested brands
    brand_objects = Brand.objects.filter(name__in=brands)
    if not brand_objects.exists():
        print(f"Warning: No brands found: {brands}")
        return {}
    
    result = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'brands_requested': brands,
            'brands_found': [brand.name for brand in brand_objects]
        },
        'summary': {},
        'relationships': {},
        'cross_brand_analysis': {}
    }
    
    # Get summary statistics
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
        
        result['summary'][brand.name] = {
            'stations_count': stations_count,
            'sensors_count': sensors_count,
            'relationships_count': relationships_count
        }
    
    result['summary']['TOTAL'] = {
        'stations_count': total_stations,
        'sensors_count': total_sensors,
        'relationships_count': total_relationships
    }
    
    if not include_details:
        return result
    
    # Get detailed relationships for each brand
    for brand in brand_objects:
        stations = Station.objects.filter(brand=brand).prefetch_related(
            Prefetch(
                'station_sensors',
                queryset=StationSensor.objects.select_related('sensor', 'sensor__brand')
            )
        ).order_by('name')
        
        brand_data = {
            'brand_info': {
                'id': brand.id,
                'name': brand.name
            },
            'stations': []
        }
        
        for station in stations:
            station_data = {
                'id': station.id,
                'name': station.name,
                'serial_number': station.serial_number,
                'status': station.status,
                'address': station.address,
                'latitude': float(station.latitude) if station.latitude else None,
                'longitude': float(station.longitude) if station.longitude else None,
                'installation_date': station.installation_date.isoformat() if station.installation_date else None,
                'last_updated_at': station.last_updated_at.isoformat() if station.last_updated_at else None,
                'sensors': []
            }
            
            # Get sensors for this station
            station_sensors = station.station_sensors.all()
            for ss in station_sensors:
                sensor = ss.sensor
                sensor_data = {
                    'id': sensor.id,
                    'type': sensor.type,
                    'unit': sensor.unit,
                    'brand': sensor.brand.name if sensor.brand else None
                }
                station_data['sensors'].append(sensor_data)
            
            brand_data['stations'].append(station_data)
        
        result['relationships'][brand.name] = brand_data
    
    # Cross-brand analysis
    cross_brand_sensors = StationSensor.objects.values('sensor__type').annotate(
        brand_count=Count('station__brand', distinct=True)
    ).filter(brand_count__gt=1)
    
    result['cross_brand_analysis']['sensors_across_brands'] = [
        {
            'sensor_type': sensor_info['sensor__type'],
            'brand_count': sensor_info['brand_count']
        }
        for sensor_info in cross_brand_sensors
    ]
    
    # Find stations with sensors from different brands
    mixed_brand_stations = Station.objects.filter(
        brand__in=brand_objects
    ).annotate(
        sensor_brand_count=Count('station_sensors__sensor__brand', distinct=True)
    ).filter(sensor_brand_count__gt=1)
    
    result['cross_brand_analysis']['mixed_brand_stations'] = [
        {
            'station_name': station.name,
            'station_brand': station.brand.name,
            'sensor_brand_count': station.sensor_brand_count
        }
        for station in mixed_brand_stations
    ]
    
    return result


def export_to_csv(data, output_file=None):
    """
    Export the relationships data to CSV format.
    
    Args:
        data (dict): The relationships data from get_station_sensor_relationships
        output_file (str): Output file path. If None, prints to stdout
    """
    if not data.get('relationships'):
        print("No relationships data to export")
        return
    
    csv_lines = []
    
    # CSV header
    csv_lines.append("Brand,Station,SerialNumber,Status,Address,Latitude,Longitude,SensorType,SensorUnit,SensorBrand")
    
    for brand_name, brand_data in data['relationships'].items():
        for station in brand_data['stations']:
            if station['sensors']:
                for sensor in station['sensors']:
                    csv_lines.append(
                        f'"{brand_name}","{station["name"]}","{station["serial_number"]}","{station["status"]}",'
                        f'"{station["address"]}",{station["latitude"] or ""},{station["longitude"] or ""},'
                        f'"{sensor["type"]}","{sensor["unit"]}","{sensor["brand"] or ""}"'
                    )
            else:
                # Station with no sensors
                csv_lines.append(
                    f'"{brand_name}","{station["name"]}","{station["serial_number"]}","{station["status"]}",'
                    f'"{station["address"]}",{station["latitude"] or ""},{station["longitude"] or ""},,,'
                )
    
    csv_content = '\n'.join(csv_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        print(f"CSV exported to: {output_file}")
    else:
        print(csv_content)


def print_summary(data):
    """Print a human-readable summary of the relationships data."""
    print("=" * 60)
    print("STATION-SENSOR RELATIONSHIPS SUMMARY")
    print("=" * 60)
    
    metadata = data.get('metadata', {})
    print(f"Generated: {metadata.get('timestamp', 'Unknown')}")
    print(f"Brands requested: {', '.join(metadata.get('brands_requested', []))}")
    print(f"Brands found: {', '.join(metadata.get('brands_found', []))}")
    print()
    
    summary = data.get('summary', {})
    if 'TOTAL' in summary:
        total = summary['TOTAL']
        print(f"TOTAL STATIONS: {total['stations_count']}")
        print(f"TOTAL SENSORS: {total['sensors_count']}")
        print(f"TOTAL RELATIONSHIPS: {total['relationships_count']}")
        print()
    
    for brand_name, brand_summary in summary.items():
        if brand_name != 'TOTAL':
            print(f"{brand_name}:")
            print(f"  Stations: {brand_summary['stations_count']}")
            print(f"  Sensors: {brand_summary['sensors_count']}")
            print(f"  Relationships: {brand_summary['relationships_count']}")
            print()
    
    # Show some cross-brand insights
    cross_brand = data.get('cross_brand_analysis', {})
    if cross_brand.get('sensors_across_brands'):
        print("Sensors used across multiple brands:")
        for sensor_info in cross_brand['sensors_across_brands'][:5]:  # Show first 5
            print(f"  • {sensor_info['sensor_type']}: {sensor_info['brand_count']} brands")
        print()


def main():
    """Main function to run the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Get station-sensor relationships for specific brands')
    parser.add_argument('--brands', nargs='+', 
                       default=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT'],
                       help='Brands to analyze (default: 3D_Paws, Allmeteo, Zentra, OTT)')
    parser.add_argument('--format', choices=['json', 'csv', 'summary'], default='summary',
                       help='Output format (default: summary)')
    parser.add_argument('--output', help='Output file path (for JSON or CSV)')
    parser.add_argument('--no-details', action='store_true', 
                       help='Exclude detailed relationship data (summary only)')
    
    args = parser.parse_args()
    
    try:
        # Get the relationships data
        data = get_station_sensor_relationships(
            brands=args.brands,
            include_details=not args.no_details
        )
        
        if args.format == 'json':
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"JSON exported to: {args.output}")
            else:
                print(json.dumps(data, indent=2))
        
        elif args.format == 'csv':
            if not args.no_details:
                export_to_csv(data, args.output)
            else:
                print("CSV format requires detailed data. Use --format summary for summary-only output.")
        
        else:  # summary format
            print_summary(data)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 