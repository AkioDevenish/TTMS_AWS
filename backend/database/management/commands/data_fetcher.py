import requests
from django.core.management.base import BaseCommand
from database.models import Measurement, Station, Sensor, Brand, StationSensor, StationHealthLog
from database.validation import DataValidator
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from dateutil import parser
import logging
import time
from django.conf import settings
import os
from logging.handlers import RotatingFileHandler
import asyncio
import concurrent.futures
import mysql.connector
from mysql.connector import Error
from django.db import transaction

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
log_file = os.path.join(log_dir, 'fetcher.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)   
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Command(BaseCommand):
    help = 'Fetches data from PAWS, Zentra, and Barani instruments and stores it in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-full-sync',
            action='store_true',
            help='Force a complete 3-month reimport for all data sources',
        )

    def handle(self, *args, **kwargs):
        logger.info("Starting data_fetcher management command")
        
        # Set environment variable if force-full-sync is requested
        if kwargs.get('force_full_sync'):
            os.environ['FORCE_SUTRON_SYNC'] = 'true'
            os.environ['FORCE_XC_SYNC'] = 'true'
            self.stdout.write(self.style.WARNING("Force full sync enabled - will reimport all data from last 3 months"))
        
        try:
            # Set Trinidad and Tobago timezone (UTC-4)
            tt_tz = timezone.get_fixed_timezone(-240)
            
            # Calculate time range from 12 hours ago to now
            end_time = timezone.now().astimezone(tt_tz)
            start_time = end_time - timedelta(hours=12)

            logger.info(f"Fetching data from {start_time} to {end_time}")

            # Format times for different APIs
            self.start_datetime = start_time.strftime("%Y-%m-%d %H:%M:%S")
            self.end_datetime = end_time.strftime("%Y-%m-%d %H:%M:%S")

            # Run fetchers concurrently (including XC Data and Sutron)
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                logger.info("Starting data fetchers")
                # Start all fetchers
                paws_future = executor.submit(self.fetch_paws_data)
                zentra_future = executor.submit(self.fetch_zentra_data)
                barani_future = executor.submit(self.fetch_barani_data)
                ott_future = executor.submit(self.fetch_ott_hydromet_data)
                xc_future = executor.submit(self.fetch_xc_data)
                sutron_future = executor.submit(self.fetch_sutron_data)

                # Wait for all fetchers to complete and check for errors
                futures = [paws_future, zentra_future, barani_future, ott_future, xc_future, sutron_future]
                concurrent.futures.wait(futures)
                
                # Check for exceptions
                for i, future in enumerate(futures):
                    try:
                        future.result()  # This will raise any exception that occurred
                    except Exception as e:
                        fetcher_names = ['PAWS', 'Zentra', 'Barani', 'OTT', 'XC Data', 'Sutron']
                        logger.error(f"Error in {fetcher_names[i]} fetcher: {e}")
                        self.stdout.write(self.style.ERROR(f"Error in {fetcher_names[i]} fetcher: {e}"))
                
                logger.info("All data fetchers completed")
                
        except Exception as e:
            logger.error(f"Error in data_fetcher command: {str(e)}")
            raise

    def get_stations_by_brand(self, brand_name):
        """Get stations by brand name directly from database"""
        return Station.objects.filter(brand__name=brand_name)

    def get_sensor_map(self):
        """Get sensor mapping directly from database"""
        sensors = Sensor.objects.all()
        return {sensor.type: sensor.id for sensor in sensors}

    def fetch_sutron_data(self):
        """Fetch data from Sutron MySQL database"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting Sutron Data Fetch ==='))
        
        # Sutron database configuration (actually xc_data database)
        SUTRON_DB_CONFIG = {
            'host': '10.222.3.39',
            'port': 3306,
            'database': 'xc_data',
            'user': 'root',
            'password': 'My$Ql2',
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': True,
            'connect_timeout': 30,
            'read_timeout': 30,
            'write_timeout': 30
        }
        
        try:
            # Connect to Sutron database
            self.stdout.write("Connecting to Sutron database...")
            connection = self.connect_to_sutron_db(SUTRON_DB_CONFIG)
            if not connection:
                logger.error("Failed to connect to Sutron database")
                self.stdout.write(self.style.ERROR("Failed to connect to Sutron database"))
                return
            
            self.stdout.write("Connected to Sutron database successfully!")
            
            # Get last sync time (3 months ago if no measurements exist)
            self.stdout.write("Getting last sync time...")
            last_sync_time = self.get_last_sutron_sync_time()
            logger.info(f"Last Sutron sync time: {last_sync_time}")
            self.stdout.write(f"Last Sutron sync time: {last_sync_time}")
            
            # Run synchronization with transaction
            self.stdout.write("Starting Sutron synchronization...")
            with transaction.atomic():
                # Sync brands
                self.stdout.write("Syncing Sutron brands...")
                brands = self.sync_sutron_brands()
                self.stdout.write(f"Synced {len(brands)} brands")
                
                # Sync stations
                self.stdout.write("Syncing Sutron stations...")
                stations = self.sync_sutron_stations(connection, brands)
                self.stdout.write(f"Synced {len(stations)} stations")
                
                # Sync sensors
                self.stdout.write("Syncing Sutron sensors...")
                sensors = self.sync_sutron_sensors(connection, stations)
                self.stdout.write(f"Synced {len(sensors)} sensors")
                
                # Ensure all historical station-sensor relationships are established
                self.stdout.write("Ensuring historical station-sensor relationships...")
                self.ensure_historical_station_sensor_relationships(connection, stations, sensors)
                
                # Sync measurements (with safety limit)
                self.stdout.write("Syncing Sutron measurements...")
                measurement_count = self.sync_sutron_measurements(connection, stations, sensors, last_sync_time)
                self.stdout.write(f"Synced {measurement_count} measurements")
                
                # Sync health data (skip for now as no health table exists)
                health_count = 0  # self.sync_sutron_health_data(connection, stations, last_sync_time)
                
                logger.info(f"Sutron data synchronization completed successfully!")
                logger.info(f"Total measurements synced: {measurement_count}")
                logger.info(f"Total health records synced: {health_count}")
                
                self.stdout.write(f"Sutron data synchronization completed successfully!")
                self.stdout.write(f"Total measurements synced: {measurement_count}")
                self.stdout.write(f"Total health records synced: {health_count}")
            
            connection.close()
            self.stdout.write(self.style.SUCCESS("=== Sutron Data Fetch Complete ===\n"))
            
        except Exception as e:
            logger.error(f"Error during Sutron data synchronization: {e}")
            self.stdout.write(self.style.ERROR(f"Error during Sutron data synchronization: {e}"))
            import traceback
            traceback.print_exc()

    def connect_to_sutron_db(self, config):
        """Connect to Sutron MySQL database"""
        try:
            self.stdout.write(f"Attempting to connect to {config['host']}:{config['port']}...")
            connection = mysql.connector.connect(**config)
            
            # Test the connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            self.stdout.write("Database connection test successful!")
            return connection
        except Error as e:
            logger.error(f"Error connecting to Sutron database: {e}")
            self.stdout.write(self.style.ERROR(f"Database connection error: {e}"))
            return None
        except Exception as e:
            logger.error(f"Unexpected error connecting to Sutron database: {e}")
            self.stdout.write(self.style.ERROR(f"Unexpected database error: {e}"))
            return None

    def get_last_sutron_sync_time(self):
        """Get the last sync time from local database for Sutron data"""
        try:
            # Check if we want to force a complete 3-month reimport
            # This can be useful when stations/sensors have been added or when fixing sync issues
            force_full_sync = os.environ.get('FORCE_SUTRON_SYNC', 'false').lower() == 'true'
            
            if force_full_sync:
                self.stdout.write("FORCE_SUTRON_SYNC environment variable set - performing full 3-month reimport")
                return timezone.now() - timedelta(days=90)
            
            # Get the most recent measurement timestamp
            latest_measurement = Measurement.objects.order_by('-created_at').first()
            if latest_measurement:
                return latest_measurement.created_at
            
            # Fallback to 3 months ago if no measurements exist
            return timezone.now() - timedelta(days=90)
            
        except Exception as e:
            logger.error(f"Error getting last Sutron sync time: {e}")
            return timezone.now() - timedelta(days=90)

    def sync_sutron_brands(self):
        """Sync brands from Sutron"""
        brands = {}
        try:
            # Get or create Sutron brand
            sutron_brand, created = Brand.objects.get_or_create(
                name="Sutron",
                defaults={'description': 'Data imported from Sutron system'}
            )
            brands['Sutron'] = sutron_brand
            
            if created:
                self.stdout.write(f"Created new brand: Sutron")
            
            return brands
        except Exception as e:
            logger.error(f"Error syncing Sutron brands: {e}")
            return {}

    def sync_sutron_stations(self, connection, brands):
        """Sync stations from Sutron"""
        stations = {}
        try:
            cursor = connection.cursor(dictionary=True)
            # Use the correct table name and column names from xc_data database
            cursor.execute("""
                SELECT 
                    STATION_ID as station_id,
                    SITE_LONG_NAME as station_name,
                    SITE_TYPE as station_type,
                    LATITUDE as latitude,
                    LONGITUDE as longitude,
                    ELEVATION as elevation,
                    INSTALLATION_DATE as installation_date,
                    ENABLED as enabled,
                    STATUS as status,
                    LAST_UPDATE as last_communication,
                    AGENCY as agency,
                    CITY as city,
                    STATE as state,
                    COUNTRY as country
                FROM xc_sites 
                WHERE ENABLED = 'Y'
                ORDER BY STATION_ID
            """)
            sutron_stations = cursor.fetchall()
            cursor.close()
            
            self.stdout.write(f"Found {len(sutron_stations)} enabled stations in xc_sites table")
            
            for sutron_station in sutron_stations:
                # Use STATION_ID as name since descriptive fields are empty in the database
                station_name = sutron_station['station_id']
                
                station, created = Station.objects.get_or_create(
                    serial_number=sutron_station['station_id'],
                    defaults={
                        'name': station_name,
                        'brand': brands.get('Sutron'),
                        'latitude': sutron_station.get('latitude', 0.0),
                        'longitude': sutron_station.get('longitude', 0.0),
                        'elevation': sutron_station.get('elevation', 0.0),
                        'status': 'Active'
                    }
                )
                
                # Update existing stations with latest info
                if not created:
                    station.name = station_name
                    station.latitude = sutron_station.get('latitude', 0.0)
                    station.longitude = sutron_station.get('longitude', 0.0)
                    station.elevation = sutron_station.get('elevation', 0.0)
                    station.save()
                
                stations[sutron_station['station_id']] = station
                
                if created:
                    self.stdout.write(f"Created new Sutron station: {station.name}")
                else:
                    self.stdout.write(f"Updated existing Sutron station: {station.name}")
            
            return stations
        except Exception as e:
            logger.error(f"Error syncing Sutron stations: {e}")
            return {}

    def sync_sutron_sensors(self, connection, stations):
        """Sync sensors from Sutron"""
        sensors = {}
        try:
            cursor = connection.cursor(dictionary=True)
            # Use the correct table and column names from xc_data database
            cursor.execute("""
                SELECT DISTINCT 
                    SENSORNAME as sensor_name,
                    UNITS as units,
                    DESCRIPTION as description
                FROM xc_sitesensors 
                WHERE ENABLED = 'Y'
                ORDER BY SENSORNAME
            """)
            sensor_types = cursor.fetchall()
            cursor.close()
            
            self.stdout.write(f"Found {len(sensor_types)} enabled sensors in xc_sitesensors table")
            
            for sensor_row in sensor_types:
                sensor_name = sensor_row['sensor_name']
                units = sensor_row['units'] or self.get_sensor_unit(sensor_name)
                
                sensor, created = Sensor.objects.get_or_create(
                    type=sensor_name,
                    defaults={'unit': units}
                )
                
                # Update existing sensors with latest info
                if not created:
                    sensor.unit = units
                    sensor.save()
                
                sensors[sensor_name] = sensor
                
                if created:
                    self.stdout.write(f"Created new Sutron sensor: {sensor_name} ({units})")
                else:
                    self.stdout.write(f"Updated existing Sutron sensor: {sensor_name} ({units})")
            
            # Now ensure all station-sensor relationships are established for the last 3 months
            self.stdout.write("Establishing station-sensor relationships for all stations and sensors...")
            for station_id, station in stations.items():
                sensor_types = list(sensors.keys())
                self.pre_create_station_sensor_relationships(station.id, sensor_types)
                self.stdout.write(f"Established relationships for station {station.name} with {len(sensor_types)} sensors")
            
            return sensors
        except Exception as e:
            logger.error(f"Error syncing Sutron sensors: {e}")
            return {}

    def sync_sutron_measurements(self, connection, stations, sensors, last_sync_time):
        """Sync measurements from Sutron"""
        measurement_count = 0
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query for measurements after last sync time using the correct table structure
            query = """
                SELECT 
                    d.STATION_ID as station_id,
                    d.SENSORNAME as sensor_name,
                    d.TIME_TAG as timestamp,
                    d.ORIG_VALUE as value,
                    d.ED_VALUE as edited_value,
                    d.FLAG1 as flag1,
                    d.FLAG2 as flag2,
                    d.FLAG3 as flag3,
                    d.FLAG4 as flag4,
                    d.HIGH_FLAG as high_flag,
                    d.LOW_FLAG as low_flag,
                    d.ALARM_FLAG as alarm_flag
                FROM xc_data1 d
                JOIN xc_sites s ON d.STATION_ID = s.STATION_ID
                WHERE d.TIME_TAG > %s AND s.ENABLED = 'Y'
                ORDER BY d.TIME_TAG
            """
            cursor.execute(query, (last_sync_time,))
            sutron_measurements = cursor.fetchall()
            cursor.close()
            
            self.stdout.write(f"Found {len(sutron_measurements)} measurements to sync")
            
            for sutron_measurement in sutron_measurements:
                station_id = sutron_measurement['station_id']
                sensor_name = sutron_measurement['sensor_name']
                
                if station_id in stations and sensor_name in sensors:
                    try:
                        # Parse timestamp
                        timestamp = parse_datetime(sutron_measurement['timestamp'])
                        if not timestamp:
                            continue
                        
                        # Round to nearest hour
                        rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                        
                        # Use edited value if available, otherwise original value
                        value = sutron_measurement.get('edited_value') or sutron_measurement.get('value')
                        
                        # Validate measurement
                        is_valid, validation_message = DataValidator.validate_measurement(
                            sensor_name, value
                        )
                        
                        # Create measurement
                        Measurement.objects.create(
                            station_id=stations[station_id].id,
                            sensor_id=sensors[sensor_name].id,
                            date=rounded_timestamp.date(),
                            time=rounded_timestamp.time(),
                            value=sutron_measurement['value'],
                            status="Successful",
                            note=f"Sutron Data Import - Validation: {validation_message}",
                            flag=is_valid,
                            created_at=timezone.now()
                        )
                        
                        measurement_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error saving Sutron measurement: {e}")
                        continue
            
            return measurement_count
        except Exception as e:
            logger.error(f"Error syncing Sutron measurements: {e}")
            return 0

    def sync_sutron_health_data(self, connection, stations, last_sync_time):
        """Sync health data from Sutron"""
        health_count = 0
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query for health data after last sync time
            query = """
                SELECT h.*, s.station_id 
                FROM health_data h 
                JOIN stations s ON h.station_id = s.station_id 
                WHERE h.timestamp > %s AND s.status = 'active'
                ORDER BY h.timestamp
            """
            cursor.execute(query, (last_sync_time,))
            sutron_health = cursor.fetchall()
            cursor.close()
            
            for sutron_health_record in sutron_health:
                station_id = sutron_health_record['station_id']
                
                if station_id in stations:
                    try:
                        # Parse timestamp
                        timestamp = parse_datetime(sutron_health_record['timestamp'])
                        if not timestamp:
                            continue
                        
                        # Create health log entry
                        StationHealthLog.objects.create(
                            station_id=stations[station_id].id,
                            battery_status=sutron_health_record.get('battery_status', 'Unknown'),
                            connectivity_status=sutron_health_record.get('connectivity_status', 'Unknown'),
                            created_at=timestamp
                        )
                        
                        health_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error saving Sutron health data: {e}")
                        continue
            
            return health_count
        except Exception as e:
            logger.error(f"Error syncing Sutron health data: {e}")
            return 0

    def fetch_xc_data(self):
        """Fetch data from XC Data MySQL database"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting XC Data Fetch ==='))
        
        # XC Data database configuration
        XC_DB_CONFIG = {
            'host': '10.222.3.39',
            'port': 3306,
            'database': 'xc_data',
            'user': 'root',
            'password': 'My$Ql2',
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': True
        }
        
        try:
            # Connect to XC Data database
            connection = self.connect_to_xc_db(XC_DB_CONFIG)
            if not connection:
                logger.error("Failed to connect to XC Data database")
                return
            
            # Get last sync time (3 months ago if no measurements exist)
            last_sync_time = self.get_last_xc_sync_time()
            logger.info(f"Last XC sync time: {last_sync_time}")
            
            # Run synchronization with transaction
            with transaction.atomic():
                # Sync brands
                brands = self.sync_xc_brands()
                
                # Sync sites
                sites = self.sync_xc_sites(connection, brands)
                
                # Sync sensors
                sensors = self.sync_xc_sensors(connection, sites)
                
                # Sync measurements
                measurement_count = self.sync_xc_measurements(connection, sites, sensors, last_sync_time)
                
                # Sync health data
                health_count = self.sync_xc_health_data(connection, sites, last_sync_time)
                
                logger.info(f"XC Data synchronization completed successfully!")
                logger.info(f"Total measurements synced: {measurement_count}")
                logger.info(f"Total health records synced: {health_count}")
            
            connection.close()
            self.stdout.write(self.style.SUCCESS("=== XC Data Fetch Complete ===\n"))
            
        except Exception as e:
            logger.error(f"Error during XC data synchronization: {e}")
            self.stdout.write(self.style.ERROR(f"Error during XC data synchronization: {e}"))

    def connect_to_xc_db(self, config):
        """Connect to XC Data MySQL database"""
        try:
            connection = mysql.connector.connect(**config)
            return connection
        except Error as e:
            logger.error(f"Error connecting to XC Data database: {e}")
            return None

    def get_last_xc_sync_time(self):
        """Get the last sync time from local database for XC data"""
        try:
            # Check if we want to force a complete 3-month reimport
            force_full_sync = os.environ.get('FORCE_XC_SYNC', 'false').lower() == 'true'
            
            if force_full_sync:
                self.stdout.write("FORCE_XC_SYNC environment variable set - performing full 3-month reimport")
                return timezone.now() - timedelta(days=90)
            
            # Get the most recent measurement timestamp
            latest_measurement = Measurement.objects.order_by('-created_at').first()
            if latest_measurement:
                return latest_measurement.created_at
            
            # Fallback to 3 months ago if no measurements exist
            return timezone.now() - timedelta(days=90)
            
        except Exception as e:
            logger.error(f"Error getting last XC sync time: {e}")
            return timezone.now() - timedelta(days=90)

    def sync_xc_brands(self):
        """Sync brands from XC Data"""
        brands = {}
        try:
            # Get or create XC Data brand
            xc_brand, created = Brand.objects.get_or_create(
                name="XC Data Import",
                defaults={'description': 'Data imported from XC Data system'}
            )
            brands['XC Data Import'] = xc_brand
            
            if created:
                self.stdout.write(f"Created new brand: XC Data Import")
            
            return brands
        except Exception as e:
            logger.error(f"Error syncing XC brands: {e}")
            return {}

    def sync_xc_sites(self, connection, brands):
        """Sync sites from XC Data"""
        sites = {}
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sites WHERE status = 'active'")
            xc_sites = cursor.fetchall()
            cursor.close()
            
            for xc_site in xc_sites:
                site, created = Station.objects.get_or_create(
                    serial_number=xc_site['site_id'],
                    defaults={
                        'name': xc_site.get('site_name', f"XC Site {xc_site['site_id']}"),
                        'brand': brands.get('XC Data Import'),
                        'latitude': xc_site.get('latitude', 0.0),
                        'longitude': xc_site.get('longitude', 0.0),
                        'elevation': xc_site.get('elevation', 0.0),
                        'status': 'Active'
                    }
                )
                sites[xc_site['site_id']] = site
                
                if created:
                    self.stdout.write(f"Created new XC site: {site.name}")
            
            return sites
        except Exception as e:
            logger.error(f"Error syncing XC sites: {e}")
            return {}

    def sync_xc_sensors(self, connection, sites):
        """Sync sensors from XC Data"""
        sensors = {}
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT sensor_type FROM measurements")
            sensor_types = cursor.fetchall()
            cursor.close()
            
            for sensor_type_row in sensor_types:
                sensor_type = sensor_type_row['sensor_type']
                sensor, created = Sensor.objects.get_or_create(
                    type=sensor_type,
                    defaults={'unit': self.get_sensor_unit(sensor_type)}
                )
                sensors[sensor_type] = sensor
                
                if created:
                    self.stdout.write(f"Created new XC sensor: {sensor_type}")
            
            return sensors
        except Exception as e:
            logger.error(f"Error syncing XC sensors: {e}")
            return {}

    def sync_xc_measurements(self, connection, sites, sensors, last_sync_time):
        """Sync measurements from XC Data"""
        measurement_count = 0
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query for measurements after last sync time
            query = """
                SELECT m.*, s.site_id 
                FROM measurements m 
                JOIN sites s ON m.site_id = s.site_id 
                WHERE m.timestamp > %s AND s.status = 'active'
                ORDER BY m.timestamp
            """
            cursor.execute(query, (last_sync_time,))
            xc_measurements = cursor.fetchall()
            cursor.close()
            
            for xc_measurement in xc_measurements:
                site_id = xc_measurement['site_id']
                sensor_type = xc_measurement['sensor_type']
                
                if site_id in sites and sensor_type in sensors:
                    try:
                        # Parse timestamp
                        timestamp = parse_datetime(xc_measurement['timestamp'])
                        if not timestamp:
                            continue
                        
                        # Round to nearest hour
                        rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                        
                        # Validate measurement
                        is_valid, validation_message = DataValidator.validate_measurement(
                            sensor_type, xc_measurement['value']
                        )
                        
                        # Create measurement
                        Measurement.objects.create(
                            station_id=sites[site_id].id,
                            sensor_id=sensors[sensor_type].id,
                            date=rounded_timestamp.date(),
                            time=rounded_timestamp.time(),
                            value=xc_measurement['value'],
                            status="Successful",
                            note=f"XC Data Import - Validation: {validation_message}",
                            flag=is_valid,
                            created_at=timezone.now()
                        )
                        
                        measurement_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error saving XC measurement: {e}")
                        continue
            
            return measurement_count
        except Exception as e:
            logger.error(f"Error syncing XC measurements: {e}")
            return 0

    def sync_xc_health_data(self, connection, sites, last_sync_time):
        """Sync health data from XC Data"""
        health_count = 0
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query for health data after last sync time
            query = """
                SELECT h.*, s.site_id 
                FROM health_data h 
                JOIN sites s ON h.site_id = s.site_id 
                WHERE h.timestamp > %s AND s.status = 'active'
                ORDER BY h.timestamp
            """
            cursor.execute(query, (last_sync_time,))
            xc_health = cursor.fetchall()
            cursor.close()
            
            for xc_health_record in xc_health:
                site_id = xc_health_record['site_id']
                
                if site_id in sites:
                    try:
                        # Parse timestamp
                        timestamp = parse_datetime(xc_health_record['timestamp'])
                        if not timestamp:
                            continue
                        
                        # Create health log entry
                        StationHealthLog.objects.create(
                            station_id=sites[site_id].id,
                            battery_status=xc_health_record.get('battery_status', 'Unknown'),
                            connectivity_status=xc_health_record.get('connectivity_status', 'Unknown'),
                            created_at=timestamp
                        )
                        
                        health_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error saving XC health data: {e}")
                        continue
            
            return health_count
        except Exception as e:
            logger.error(f"Error syncing XC health data: {e}")
            return 0

    def fetch_paws_data(self):
        """Fetch data from PAWS instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting PAWS Data Fetch ==='))
        
        # Use the same time range as defined in handle method
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)
        
        # Format times for PAWS API
        start = START_DATE.strftime("%Y-%m-%dT%H:%M:%S")
        end = END_DATE.strftime("%Y-%m-%dT%H:%M:%S")

        portal_url = "http://3d-trinidad.icdp.ucar.edu"
        user_email = "jerome.ramirez@metoffice.gov.tt"
        api_key = "sVALwcRMyQmjtwYpDPW-"

        # Get stations directly from database
        paws_stations = self.get_stations_by_brand("3D_Paws")
        if not paws_stations.exists():
            logger.warning("No stations found for brand '3D Paws'.")
            return

        sensor_map = self.get_sensor_map()

        for station in paws_stations:
            self.stdout.write(f"Fetching data for PAWS station: {station.name} (Serial: {station.serial_number})")
            
            # Use fetch_paws_station_data instead of direct API call
            data = self.fetch_paws_station_data(
                portal_url=portal_url,
                station_id=station.serial_number,  # Use serial_number instead of ID
                start=start,
                end=end,
                user_email=user_email,
                api_key=api_key
            )

            if data:
                try:
                    saved_data = self.process_paws_data(station.id, data, sensor_map)
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully processed data for station {station.name}"
                    ))
                except Exception as e:
                    logger.error(f"Error processing data for station {station.name}: {str(e)}")
            else:
                logger.warning(f"No data received for station {station.name}")

        self.stdout.write(self.style.SUCCESS("=== PAWS Data Fetch Complete ===\n"))

    def fetch_zentra_data(self):
        """Fetch data from Zentra instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting Zentra Data Fetch ==='))

        BASE_URL = "https://zentracloud.com/api/v4/get_readings/"
        API_TOKEN = "3db9d133d878433b0c7f4a26adfa566426921e0e"
        
        headers = {"Authorization": f"Token {API_TOKEN}"}

        # Use the same time range as defined in handle method
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)

        # Get stations directly from database
        zentra_stations = self.get_stations_by_brand("Zentra")
        if not zentra_stations.exists():
            logger.warning("No stations found for brand 'Zentra'.")
            return

        sensor_map = self.get_sensor_map()

        for station in zentra_stations:
            self.stdout.write(f"Fetching data for Zentra station: {station.name} (Serial: {station.serial_number})")
            if not station.serial_number:
                logger.warning(f"No serial number for station {station.name}")
                continue

            # Parameters for the API request
            base_params = {
                "device_sn": station.serial_number.strip(),  # Ensure clean serial number
                "start_date": START_DATE.strftime("%Y-%m-%d %H:%M:%S"),
                "end_date": END_DATE.strftime("%Y-%m-%d %H:%M:%S"),
                "output_format": "json",
                "per_page": 1000,
                "sort_by": "asc"
            }

            self.stdout.write(f"Time range: {base_params['start_date']} to {base_params['end_date']}")
            
            all_data = {'data': {}}
            page = 1
            data_found = False

            while True:
                params = {**base_params, 'page_num': page}
                response = self.fetch_zentra_station_data(BASE_URL, headers, params)
                
                if not response:
                    self.stdout.write(self.style.ERROR("No response received from API"))
                    break

                if 'data' not in response:
                    self.stdout.write(self.style.ERROR("No data field in response"))
                    self.stdout.write(f"Response structure: {response.keys()}")
                    break

                if not response['data']:
                    self.stdout.write(f"No data returned for page {page}")
                    if page == 1:
                        self.stdout.write("No measurements found in the specified time range")
                    break

                data_found = True
                # Rest of the processing remains the same
                for measurement_name, measurement_data in response['data'].items():
                    if measurement_name not in all_data['data']:
                        all_data['data'][measurement_name] = []
                    all_data['data'][measurement_name].extend(measurement_data)
                
                total_readings = sum(len(data) for data in response['data'].values())
                if total_readings < base_params['per_page']:
                    break
                    
                page += 1

            if data_found:
                saved_data = self.process_zentra_data(station.id, all_data, sensor_map)
                self.stdout.write(self.style.SUCCESS(f"Successfully processed {len(saved_data)} measurements"))
            else:
                self.stdout.write(self.style.WARNING("No data to process"))

        self.stdout.write(self.style.SUCCESS("=== Zentra Data Fetch Complete ===\n"))

    def fetch_barani_data(self):
        """Fetch data from Barani instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting Barani Data Fetch ==='))

        BASE_URL = "https://api.allmeteo.com/api/historical_data"
        TOKEN = "yaoX9GFMP9ZUvxFej6LADSeF2LpccfF+qvYCpiT+LxA="
        
        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }

        # Use the same time range as other fetchers
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)

        # Convert to Unix timestamps
        params = {
            "from_time": int(START_DATE.timestamp()),
            "to_time": int(END_DATE.timestamp())
        }

        # Get stations directly from database
        barani_stations = self.get_stations_by_brand("Allmeteo")
        if not barani_stations.exists():
            logger.warning("No stations found for brand 'Allmeteo'.")
            return

        sensor_map = self.get_sensor_map()
        
        # Debug: Log what sensor types we have in the database
        self.stdout.write(f"Available sensor types in database: {list(sensor_map.keys())}")
        self.stdout.write(f"Available validation thresholds: {list(DataValidator.get_all_thresholds().keys())}")

        for station in barani_stations:
            if not station.serial_number:
                logger.warning(f"No serial number for station {station.name}")
                continue

            # Prepare request body with station's device ID
            form_data = {
                "devices": (None, f'["{station.serial_number.strip()}"]')  # Ensure clean serial number
            }

            self.stdout.write(f"Fetcring data for Barani station: {station.name} (Serial: {station.serial_number})")
            
            try:
                response = requests.post(
                    BASE_URL,
                    headers=headers,
                    params=params,
                    files=form_data
                )

                if response.status_code == 200:
                    data = response.json()
                    saved_data = self.process_barani_data(station.id, data, sensor_map)
                    self.stdout.write(self.style.SUCCESS(f"  Successfully processed {len(saved_data)} measurements"))
                else:
                    self.stdout.write(self.style.ERROR(f"  Failed to fetch data. Status code: {response.status_code}"))
                    self.stdout.write(f"  Response content: {response.text}")

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"  Request error: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("=== Barani Data Fetch Complete ===\n"))

    def fetch_ott_hydromet_data(self):
        """Fetch data from OTT Hydromet instruments"""
        self.stdout.write(self.style.SUCCESS('\n=== Starting OTT Hydromet Data Fetch ==='))
        logger.info('Starting OTT Hydromet Data Fetch')

        BASE_URL = "https://www.hydrometcloud.com/Data/rest/api/"
        API_KEY = "3235DzYLcYfYD1S8"
        CLIENT_ID = "207"
        HEADERS = {
            "api-key": API_KEY,
            "clientId": str(CLIENT_ID)
        }

        # Use the same time range as other fetchers
        START_DATE = parse_datetime(self.start_datetime)
        END_DATE = parse_datetime(self.end_datetime)
        start_time = START_DATE.strftime("%Y-%m-%d %H:%M:%S")
        end_time = END_DATE.strftime("%Y-%m-%d %H:%M:%S")

        # List of stations with API IDs and database IDs
        stations = [
            {"api_id": 2303, "db_id": 28, "name": "POS_SAT"},
            {"api_id": 2304, "db_id": 29, "name": "SYNOP_SAT"},
            {"api_id": 2305, "db_id": 30, "name": "TOCO_SAT"},
        ]

        sensor_map = self.get_sensor_map()

        for station in stations:
            self.stdout.write(f"Fetching sensors for OTT station: {station['name']} (API ID: {station['api_id']}, DB ID: {station['db_id']})")
            sensors_url = f"{BASE_URL}sensors?stationId={station['api_id']}"
            sensors_resp = requests.get(sensors_url, headers=HEADERS)
            logger.info(f"Fetching sensors for OTT station: {station['name']} (API ID: {station['api_id']}) - API status: {sensors_resp.status_code}")
            self.stdout.write(f"  Sensors API status: {sensors_resp.status_code}, response: {sensors_resp.text[:300]}")
            if sensors_resp.status_code != 200:
                logger.error(f"Failed to fetch sensors for OTT station {station['api_id']} - Status code: {sensors_resp.status_code}")
                self.stdout.write(self.style.ERROR(f"  Failed to fetch sensors. Status code: {sensors_resp.status_code}"))
                continue
            sensors = sensors_resp.json()
            if not sensors:
                logger.warning(f"No sensors returned for OTT station {station['api_id']}")
                continue
                
            # Debug: print all sensor names for this station
            sensor_names = [s.get('sensorName') for s in sensors]
            logger.info(f"OTT station {station['name']} (API ID: {station['api_id']}): sensors found: {sensor_names}")
            
            # Pre-create all station-sensor relationships at once (more efficient)
            station_obj = Station.objects.filter(id=station['db_id']).first()
            if station_obj:
                self.pre_create_station_sensor_relationships(station_obj.id, sensor_names)
            else:
                logger.warning(f"Station with DB ID {station['db_id']} not found in database, skipping")
                continue
            
            # Collect all sensor data first, then process health data
            all_measurements_by_hour = {}
            
            for sensor in sensors:
                sensor_name = sensor['sensorName']
                self.stdout.write(f"  Fetching data for sensor: {sensor_name}")
                data_url = (
                    f"{BASE_URL}sensordata?stationId={station['api_id']}&sensorName={sensor_name}"
                    f"&startTime={start_time}&endTime={end_time}"
                )
                data_resp = requests.get(data_url, headers=HEADERS)
                logger.info(f"Fetching data for OTT station {station['api_id']} sensor {sensor_name} - API status: {data_resp.status_code}")
                self.stdout.write(f"    Data API status: {data_resp.status_code}, response: {data_resp.text[:300]}")
                if data_resp.status_code != 200:
                    logger.error(f"Failed to fetch data for OTT station {station['api_id']} sensor {sensor_name} - Status code: {data_resp.status_code}")
                    self.stdout.write(self.style.ERROR(f"    Failed to fetch data. Status code: {data_resp.status_code}"))
                    continue
                data = data_resp.json()
                if not data or not data.get('sensorData'):
                    logger.warning(f"No data returned for OTT station {station['api_id']} sensor {sensor_name}")
                    continue
                
                # Save/process the data and collect for health processing
                try:
                    processed, measurements_by_hour = self.process_ott_hydromet_data(station_obj.id, sensor_name, data, sensor_map)
                    if not processed:
                        logger.warning(f"No measurements saved for OTT station {station['api_id']} sensor {sensor_name}")
                    else:
                        # Merge measurements into the main collection
                        for hour, sensors_data in measurements_by_hour.items():
                            if hour not in all_measurements_by_hour:
                                all_measurements_by_hour[hour] = {}
                            all_measurements_by_hour[hour].update(sensors_data)
                    
                    self.stdout.write(self.style.SUCCESS(f"    Successfully processed {len(processed)} measurements for {sensor_name}"))
                except Exception as e:
                    logger.error(f"Error processing data for OTT station {station['api_id']} sensor {sensor_name}: {e}")
                    self.stdout.write(self.style.ERROR(f"    Error processing data: {e}"))
            
            # Process health data with all collected sensor data
            if all_measurements_by_hour:
                for rounded_hour in all_measurements_by_hour.keys():
                    self.process_station_health(station_obj.id, all_measurements_by_hour, rounded_hour, "OTT")

        self.stdout.write(self.style.SUCCESS("=== OTT Hydromet Data Fetch Complete ===\n"))

    def fetch_paws_station_data(self, portal_url, station_id, start, end, user_email, api_key):
        """Fetch data for a specific PAWS station"""
        url = f"{portal_url}/api/v1/data/{station_id}?start={start}&end={end}&email={user_email}&api_key={api_key}"
        try:
            max_retries = 3
            retry_delay = 5  # seconds
            
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, verify=False, timeout=30, allow_redirects=True)
                    
                    if response.status_code == 403:
                        logger.error(
                            f"Authentication failed for PAWS station {station_id}. "
                            f"Status: {response.status_code}, "
                            f"Response: {response.text[:200]}"  # Log first 200 chars of response
                        )
                        # Try to get historical data from database instead
                        historical_data = self.get_historical_data(station_id, start, end)
                        if historical_data:
                            logger.info(f"Using historical data for station {station_id}")
                            return historical_data
                        return None
                        
                    response.raise_for_status()
                    data = response.json()
                    
                    if not isinstance(data, dict) or 'features' not in data:
                        logger.error(f"Invalid data structure received for station {station_id}")
                        return None
                    
                    return data
                    
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed for station {station_id}: {str(e)}")
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"All attempts failed for station {station_id}: {str(e)}")
                        self.stdout.write(self.style.ERROR(f"Failed to fetch data for station {station_id}: {str(e)}"))
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching data for PAWS station {station_id}: {str(e)}")
            return None

    def get_historical_data(self, station_id, start, end):
        """Get historical data from database when API fails"""
        try:
            from database.models import Measurement
            
            measurements = Measurement.objects.filter(
                station_id=station_id,
                date__gte=start.split('T')[0],
                date__lte=end.split('T')[0]
            ).order_by('date', 'time')
            
            if measurements.exists():
                # Format data to match API response structure
                return {
                    'features': [{
                        'properties': {
                            'data': [{
                                'time': f"{m.date}T{m.time}",
                                'measurements': {
                                    m.sensor.type: m.value
                                }
                            } for m in measurements]
                        }
                    }]
                }
            return None
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            return None

    def fetch_zentra_station_data(self, base_url, headers, params, max_retries=5, initial_delay=60):
        """Fetch data from Zentra API with retry logic"""
        for attempt in range(max_retries):
            try:
                self.stdout.write(f"  Attempt {attempt + 1} of {max_retries}")
                self.stdout.write(f"  Request URL: {base_url}")
                self.stdout.write(f"  Request params: {params}")
                response = requests.get(base_url, headers=headers, params=params)
                self.stdout.write(f"  Response status code: {response.status_code}")

                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS("  Successfully fetched data from Zentra API"))
                    response_data = response.json()
                    self.stdout.write("  Raw API Response:")
                    self.stdout.write(str(response_data)[:1000])  # Print first 1000 chars of response
                    return response_data
                elif response.status_code == 401:
                    self.stdout.write(self.style.ERROR("  Authentication failed. Please check your API token."))
                    self.stdout.write(f"  Response: {response.text}")
                    return None
                elif response.status_code == 403:
                    self.stdout.write(self.style.ERROR("  Forbidden. You might not have permission to access this resource."))
                    self.stdout.write(f"  Response: {response.text}")
                    return None
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', initial_delay))
                    self.stdout.write(self.style.WARNING(f"  Rate limit exceeded. Retrying in {retry_after} seconds..."))
                    time.sleep(retry_after)
                else:
                    self.stdout.write(self.style.ERROR(f"  Unexpected status code: {response.status_code}"))
                    if response.text:
                        self.stdout.write(f"  Response: {response.text}")
                    return None
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"  Request error: {str(e)}"))
                return None

        self.stdout.write(self.style.ERROR(f"  Max retries ({max_retries}) reached. Unable to fetch data."))
        return None

    def process_paws_data(self, station_id, raw_data, sensor_map):
        """Process and save PAWS data"""
        processed_data = []
        measurements_by_hour = {}
        
        if isinstance(raw_data, dict):
            features = raw_data.get("features", [])
            self.stdout.write(f"Number of features: {len(features)}")
            
            if features:
                properties = features[0].get("properties", {})
                data_entries = properties.get("data", [])
                self.stdout.write(f"Number of data entries: {len(data_entries)}")
                
                # First, collect all measurements for each hour
                for entry in data_entries:
                    measurements = entry.get("measurements", {})
                    timestamp = entry.get("time")
                    
                    if timestamp and measurements:
                        # Parse timestamp without timezone adjustment
                        entry_time = parser.parse(timestamp)
                        rounded_hour = self.round_to_nearest_hour(entry_time.isoformat())
                        
                        if rounded_hour not in measurements_by_hour:
                            measurements_by_hour[rounded_hour] = {}
                        
                        for sensor_type, value in measurements.items():
                            if sensor_type not in measurements_by_hour[rounded_hour]:
                                measurements_by_hour[rounded_hour][sensor_type] = []
                            
                            measurements_by_hour[rounded_hour][sensor_type].append({
                                'timestamp': entry_time,
                                'value': value
                            })
                
                # Pre-create all necessary station-sensor relationships for this station
                all_sensor_types = set()
                for rounded_hour in measurements_by_hour:
                    all_sensor_types.update(measurements_by_hour[rounded_hour].keys())
                
                # Pre-create relationships for all sensors found in this data
                self.pre_create_station_sensor_relationships(station_id, list(all_sensor_types))
                
                # Now process and save measurements for each hour
                for rounded_hour in measurements_by_hour:
                    for sensor_type, readings in measurements_by_hour[rounded_hour].items():
                        sensor_id = sensor_map.get(sensor_type)
                        if sensor_id:
                            # Relationship already created above, no need to check again
                            
                            # Get the reading closest to the rounded hour
                            closest_reading = min(readings, 
                                key=lambda x: abs(x['timestamp'] - rounded_hour))
                            
                            try:
                                # Validate the measurement value using the sensor_type from the database
                                is_valid, validation_message = DataValidator.validate_measurement(sensor_type, closest_reading['value'])
                                
                                # Set the flag based on validation result
                                flag = is_valid
                                
                                # Create note with validation information
                                note = f"Data Acquired - Validation: {validation_message}"
                                
                                Measurement.objects.create(
                                    station_id=station_id,
                                    sensor_id=sensor_id,
                                    date=rounded_hour.date(),
                                    time=rounded_hour.time(),
                                    value=closest_reading['value'],
                                    status="Successful",
                                    note=note,
                                    flag=flag,
                                    created_at=timezone.now()
                                )
                                
                                # Log validation result
                                if is_valid:
                                    processed_data.append(
                                        f"Saved valid PAWS measurement for station {station_id} "
                                        f"sensor {sensor_type} at {rounded_hour}"
                                    )
                                    self.stdout.write(
                                        f"Saved valid measurement: {sensor_type} = {closest_reading['value']} "
                                        f"at {rounded_hour}"
                                    )
                                else:
                                    processed_data.append(
                                        f"Saved invalid PAWS measurement for station {station_id} "
                                        f"sensor {sensor_type} at {rounded_hour} (flagged)"
                                    )
                                    self.stdout.write(
                                        self.style.WARNING(f"Saved invalid measurement: {sensor_type} = {closest_reading['value']} "
                                        f"at {rounded_hour} - {validation_message}")
                                    )
                            except Exception as e:
                                logger.error(f"Error saving measurement: {e}")
                                self.stdout.write(self.style.ERROR(f"Error saving measurement: {e}"))
        
        # After processing measurements, process health data
        for rounded_hour in measurements_by_hour.keys():
            self.process_station_health(station_id, measurements_by_hour, rounded_hour, "3D_Paws")
        
        return processed_data

    def process_zentra_data(self, station_id, response_data, sensor_map):
        processed_data = []
        measurements_by_hour = {}

        try:
            # Process each measurement
            for measurement_name, measurement_data in response_data['data'].items():
                for config in measurement_data:
                    metadata = config.get("metadata", {})
                    readings = config.get("readings", [])
                    
                    # Process readings
                    for reading in readings:
                        timestamp = self.parse_datetime(reading.get("datetime"))
                        if timestamp and reading.get("value") is not None:
                            rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                            
                            if rounded_timestamp not in measurements_by_hour:
                                measurements_by_hour[rounded_timestamp] = {}
                            
                            if measurement_name not in measurements_by_hour[rounded_timestamp]:
                                measurements_by_hour[rounded_timestamp][measurement_name] = []
                            
                            measurements_by_hour[rounded_timestamp][measurement_name].append({
                                'timestamp': timestamp,
                                'value': reading["value"]
                            })

            # Process measurements and health data for each hour
            for rounded_hour in measurements_by_hour.keys():
                # Process regular measurements
                for measurement_name, readings in measurements_by_hour[rounded_hour].items():
                    closest_reading = min(readings, key=lambda x: abs(x['timestamp'] - rounded_hour))
                    
                    sensor_id = sensor_map.get(measurement_name)
                    if sensor_id:
                        try:
                            # Validate the measurement value using the measurement_name (which should match sensor types)
                            is_valid, validation_message = DataValidator.validate_measurement(measurement_name, closest_reading['value'])
                            
                            # Set the flag based on validation result
                            flag = is_valid
                            
                            # Create note with validation information
                            note = f"Data Acquired - Validation: {validation_message}"
                            
                            self.ensure_station_sensor_relationship(station_id, sensor_id)
                            Measurement.objects.create(
                                station_id=station_id,
                                sensor_id=sensor_id,
                                date=rounded_hour.date(),
                                time=rounded_hour.time(),
                                value=closest_reading['value'],
                                status="Successful",
                                note=note,
                                flag=flag,
                                created_at=timezone.now()
                            )
                            
                            # Log validation result
                            if is_valid:
                                processed_data.append(f"Saved valid measurement for station {station_id}")
                                self.stdout.write(f"Saved valid measurement: {measurement_name} = {closest_reading['value']}")
                            else:
                                processed_data.append(f"Saved invalid measurement for station {station_id} (flagged)")
                                self.stdout.write(self.style.WARNING(f"Saved invalid measurement: {measurement_name} = {closest_reading['value']} - {validation_message}"))
                        except Exception as e:
                            logger.error(f"Error saving measurement: {e}")

                # Process health data for this hour
                self.process_station_health(station_id, measurements_by_hour, rounded_hour, "Zentra")

        except Exception as e:
            logger.error(f"Error processing data: {e}")

        return processed_data

    def process_barani_data(self, station_id, response_data, sensor_map):
        """Process and save Barani data"""
        processed_data = []
        measurements_by_hour = {}

        # Log the raw response for debugging
        self.stdout.write("Raw Barani response:")
        self.stdout.write(str(response_data)[:1000])  # First 1000 chars

        try:
            # The response data is a list of measurements
            if not isinstance(response_data, list):
                logger.error("Invalid response format from Barani API")
                return []

            # Group measurements by hour
            for reading in response_data:
                timestamp_str = reading.get('timestamp')
                if not timestamp_str:
                    continue

                timestamp = parse_datetime(timestamp_str)
                if not timestamp:
                    continue

                rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                
                if rounded_timestamp not in measurements_by_hour:
                    measurements_by_hour[rounded_timestamp] = {}

                # Process each field from the reading
                for field, value in reading.items():
                    # Skip non-measurement fields
                    if field in ['sn', 'timestamp', 'device_id']:
                        continue
                    
                    try:
                        # Convert value to float if it's a measurement
                        value = float(value)
                        
                        if field not in measurements_by_hour[rounded_timestamp]:
                            measurements_by_hour[rounded_timestamp][field] = []
                        
                        measurements_by_hour[rounded_timestamp][field].append({
                            'timestamp': timestamp,
                            'value': value
                        })
                        self.stdout.write(f"Added {field} reading: {value} at {timestamp}")
                    except (ValueError, TypeError):
                        # Skip fields that can't be converted to float
                        continue

            # Save measurements for each rounded hour
            for rounded_hour, sensor_readings in measurements_by_hour.items():
                for field, readings in sensor_readings.items():
                    # Get closest reading to rounded hour
                    closest_reading = min(readings, key=lambda x: abs(x['timestamp'] - rounded_hour))
                    
                    # Try to find a matching sensor in the database
                    # First try exact match, then try partial match
                    matched_sensor = None
                    matched_sensor_id = None
                    
                    # Try exact match first (remove units and special characters)
                    clean_field = field.split(' (')[0].strip()  # Remove units like "(V)", "(°C)", etc.
                    if clean_field in sensor_map:
                        matched_sensor = clean_field
                        matched_sensor_id = sensor_map[clean_field]
                    else:
                        # Try partial match as fallback
                        for sensor_type, sensor_id in sensor_map.items():
                            if field.lower() in sensor_type.lower() or clean_field.lower() in sensor_type.lower():
                                matched_sensor = sensor_type
                                matched_sensor_id = sensor_id
                                break
                    
                    if matched_sensor and matched_sensor_id:
                            try:
                                # Debug: Log what we're validating
                                self.stdout.write(f"  Validating field '{field}' with sensor_type '{matched_sensor}' and value {closest_reading['value']}")
                                
                                # Validate the measurement value using the field name from the instrument, not the database sensor type
                                is_valid, validation_message = DataValidator.validate_measurement(field, closest_reading['value'])
                                
                                # Set the flag based on validation result
                                flag = is_valid
                                
                                # Create note with validation information
                                note = f"Data Acquired - Validation: {validation_message}"
                                
                                self.ensure_station_sensor_relationship(station_id, matched_sensor_id)
                                Measurement.objects.create(
                                    station_id=station_id,
                                    sensor_id=matched_sensor_id,
                                    date=rounded_hour.date(),
                                    time=rounded_hour.time(),
                                    value=closest_reading['value'],
                                    status="Successful",
                                    note=note,
                                    flag=flag,
                                    created_at=datetime.now()
                                )
                                
                                # Log validation result
                                if is_valid:
                                    self.stdout.write(self.style.SUCCESS(f"  Valid measurement: {field} = {closest_reading['value']}"))
                                    processed_data.append(f"Saved valid Barani measurement for station {station_id} at {rounded_hour}")
                                else:
                                    self.stdout.write(self.style.WARNING(f"  Invalid measurement: {field} = {closest_reading['value']} - {validation_message}"))
                                    processed_data.append(f"Saved invalid Barani measurement for station {station_id} at {rounded_hour} (flagged)")
                                
                                break  # Found a matching sensor, stop looking
                            except Exception as e:
                                logger.error(f"Error saving measurement: {e}")
                                self.stdout.write(self.style.ERROR(f"Error saving measurement: {e}"))

        except Exception as e:
            logger.error(f"Error processing Barani data: {e}")
            self.stdout.write(self.style.ERROR(f"Error processing Barani data: {e}"))

        # After processing measurements, process health data
        for rounded_hour in measurements_by_hour.keys():
            self.process_station_health(station_id, measurements_by_hour, rounded_hour, "Allmeteo")

        return processed_data

    def process_ott_hydromet_data(self, station_id, sensor_name, data, sensor_map):
        """Process and save OTT Hydromet data"""
        processed_data = []
        measurements_by_hour = {}

        # The station_id passed here is already the database station ID
        # No need to create or lookup the station again
        from database.models import Sensor
        from django.utils import timezone

        try:
            # The data is expected to have a 'sensorData' key with a list of measurements
            sensor_data = data.get('sensorData', [])
            self.stdout.write(f"    Raw sensor_data for {sensor_name}: {sensor_data}")
            # Debug: if this is a battery sensor, log the full data
            if 'batt' in sensor_name.lower() or 'battery' in sensor_name.lower():
                logger.info(f"OTT station {station_id} - RAW BATTERY DATA for sensor '{sensor_name}': {sensor_data}")
            if not isinstance(sensor_data, list):
                self.stdout.write(self.style.ERROR(f"  sensorData missing or not a list for {sensor_name}"))
                return [], {}

            for entry in sensor_data:
                timestamp_str = entry.get('sampleTime')
                value = entry.get('value')
                self.stdout.write(f"      Entry: sampleTime={timestamp_str}, value={value}")
                if not timestamp_str or value is None:
                    continue
                timestamp = self.parse_datetime(timestamp_str)
                if not timestamp:
                    continue
                rounded_timestamp = self.round_to_nearest_hour(timestamp.isoformat())
                if rounded_timestamp not in measurements_by_hour:
                    measurements_by_hour[rounded_timestamp] = {}
                if sensor_name not in measurements_by_hour[rounded_timestamp]:
                    measurements_by_hour[rounded_timestamp][sensor_name] = []
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    continue
                measurements_by_hour[rounded_timestamp][sensor_name].append({
                    'timestamp': timestamp,
                    'value': value
                })

            # Save measurements for each rounded hour
            for rounded_hour, sensor_readings in measurements_by_hour.items():
                for field, readings in sensor_readings.items():
                    # --- Auto-create Sensor if missing ---
                    sensor_obj, created = Sensor.objects.get_or_create(
                        type=field,
                        unit=''
                    )
                    if created:
                        sensor_map[field] = sensor_obj.id
                    sensor_id = sensor_obj.id
                    # Get closest reading to rounded hour
                    closest_reading = min(readings, key=lambda x: abs(x['timestamp'] - rounded_hour))
                    try:
                        # Validate the measurement value using the field name (which should match sensor types)
                        is_valid, validation_message = DataValidator.validate_measurement(field, closest_reading['value'])
                        
                        # Set the flag based on validation result
                        flag = is_valid
                        
                        # Create note with validation information
                        note = f"Data Acquired - Validation: {validation_message}"
                        
                        # Relationship already created above, no need to check again
                        Measurement.objects.create(
                            station_id=station_id,
                            sensor_id=sensor_id,
                            date=rounded_hour.date(),
                            time=rounded_hour.time(),
                            value=closest_reading['value'],
                            status="Successful",
                            note=note,
                            flag=flag,
                            created_at=timezone.now()
                        )
                        
                        # Log validation result
                        if is_valid:
                            self.stdout.write(f"      Saved valid measurement: station_id={station_id}, sensor={field}, value={closest_reading['value']}, time={rounded_hour}")
                            processed_data.append(f"Saved valid OTT Hydromet measurement for station {station_id} at {rounded_hour}")
                        else:
                            self.stdout.write(self.style.WARNING(f"      Saved invalid measurement: station_id={station_id}, sensor={field}, value={closest_reading['value']}, time={rounded_hour} - {validation_message}"))
                            processed_data.append(f"Saved invalid OTT Hydromet measurement for station {station_id} at {rounded_hour} (flagged)")
                    except Exception as e:
                        logger.error(f"Error saving measurement: {e}")
                        self.stdout.write(self.style.ERROR(f"Error saving measurement: {e}"))

            # Health data processing is now handled at the station level after all sensors are processed

        except Exception as e:
            logger.error(f"Error processing OTT Hydromet data: {e}")
            self.stdout.write(self.style.ERROR(f"Error processing OTT Hydromet data: {e}"))

        return processed_data, measurements_by_hour

    def pre_create_station_sensor_relationships(self, station_id, sensor_types):
        """Pre-create all necessary station-sensor relationships for a station at once"""
        try:
            from database.models import Station, Sensor, StationSensor
            
            # Get or create sensors for all types
            sensors_to_create = []
            for sensor_type in sensor_types:
                sensor, created = Sensor.objects.get_or_create(
                    type=sensor_type,
                    defaults={'unit': self.get_sensor_unit(sensor_type)}
                )
                if created:
                    self.stdout.write(f"Created new sensor: {sensor_type}")
                sensors_to_create.append(sensor)
            
            # Get all existing relationships for this station
            existing_relationships = set(
                StationSensor.objects.filter(station_id=station_id)
                .values_list('sensor_id', flat=True)
            )
            
            # Create missing relationships in bulk
            new_relationships = []
            for sensor in sensors_to_create:
                if sensor.id not in existing_relationships:
                    new_relationships.append(StationSensor(
                        station_id=station_id,
                        sensor_id=sensor.id
                    ))
            
            if new_relationships:
                StationSensor.objects.bulk_create(new_relationships, ignore_conflicts=True)
                self.stdout.write(f"Created {len(new_relationships)} new StationSensor relationships for station {station_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error pre-creating station-sensor relationships: {e}")
            return False

    def ensure_station_sensor_relationship(self, station_id, sensor_id):
        """Ensure station-sensor relationship exists and fix sensor data if needed
        
        NOTE: This method should only be used for individual sensor setup, not during bulk data processing.
        For bulk processing, use pre_create_station_sensor_relationships() instead.
        """
        try:
            # Get the sensor
            sensor = Sensor.objects.get(id=sensor_id)
            
            # Fix missing unit if needed
            if not sensor.unit:
                unit = self.get_sensor_unit(sensor.type)
                if unit:
                    sensor.unit = unit
                    sensor.save()
                    self.stdout.write(f"Updated missing unit for sensor {sensor.type} to {unit}")
            
            # Create or get the relationship (this is safe to call multiple times)
            # but we should minimize calls during bulk processing
            relationship, created = StationSensor.objects.get_or_create(
                station_id=station_id,
                sensor_id=sensor_id
            )
            
            if created:
                self.stdout.write(f"Created new StationSensor relationship for station {station_id} and sensor {sensor_id}")
            # Don't log every time - only log when actually creating new relationships
            
        except Exception as e:
            logger.error(f"Error creating station-sensor relationship: {e}")

    def get_sensor_unit(self, sensor_type):
        """Helper function to get the unit for a sensor type"""
        sensor_units = {
            # Temperature sensors
            'bt1': '°C',
            'mt1': '°C',
            'temperature': '°C',
            'Air Temperature': '°C',
            'Maximum Air Temperature': '°C',
            'Minimum Air Temperature': '°C',
            'Dew Point': '°C',
            'Soil Temp (15cm)': '°C',
            'RH Sensor Temperature': '°C',
            
            # Pressure sensors
            'bp1': 'hPa',
            'pressure': 'hPa',
            'Barometric Pressure': 'hPa',
            'Baro Tendency': 'hPa',
            'Atmospheric Pressure': 'kPa',
            'Reference Pressure': 'kPa',
            'Vapor Pressure Deficit': 'kPa',
            
            # Wind sensors
            'ws': 'm/s',
            'wd': '°',
            'wind_ave10': 'm/s',
            'wind_max10': 'm/s',
            'wind_min10': 'm/s',
            'dir_ave10': '°',
            'dir_max10': '°',
            'dir_hi10': '°',
            'dir_lo10': '°',
            'Wind Speed': 'm/s',
            'Wind Direction': '°',
            'Gust Speed': 'm/s',
            'Gust Direction': '°',
            'Wind Speed Average': 'm/s',
            'Wind Speed Inst': 'm/s',
            'Wind Dir Average': '°',
            'Wind Dir Inst': '°',
            
            # Precipitation sensors
            'rg': 'mm',
            'Precipitation': 'mm',
            '5 min rain': 'mm',
            'Daily Rain': 'mm',
            'Max Precipitation Rate': 'mm/h',
            'rain_counter': 'mm',
            'rain_intensity_max': 'mm/h',
            
            # Solar radiation sensors
            'sv1': 'W/m²',
            'si1': 'W/m²',
            'su1': 'W/m²',
            'irradiation': 'W/m²',
            'irr_max': 'W/m²',
            'Solar Radiation': 'W/m²',
            'Solar Radiation Avg': 'W/m²',
            'Solar Radiation Total': 'W/m²',
            
            # Humidity sensors
            'humidity': '%',
            'Relative Humidity': '%',
            
            # Battery and connectivity sensors
            'battery': 'V',
            'bpc': '%',
            'css': 'dBm',
            'Battery': 'V',
            'Battery Percent': '%',
            
            # Other sensors
            'Leaf Wetness': '%',
            'Soil Moisture (10cm)': '%',
            'Soil Moisture (20cm)': '%',
            'Soil Moisture (30cm)': '%',
            'Hours of Sunshine': 'hr',
            'EvapoTranspiration': 'mm',
            'Lightning Activity': 'binary',
            'Lightning Distance': 'km',
            'X-axis Level': '°',
            'Y-axis Level': '°'
        }
        return sensor_units.get(sensor_type, '')

    def process_station_health(self, station_id, measurements_by_hour, rounded_hour, brand_name):
        """Process health-related measurements for a station, checking all possible battery fields and logging available fields for debugging."""
        try:
            # Initialize status values
            battery_status = "Unknown"
            connectivity_status = "Unknown"

            # Expanded list of possible battery fields
            battery_fields_by_brand = {
                "3D_Paws": [
                    'bpc', 'Battery Percent', 'Battery Voltage', 'battery', 'Battery',
                    'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct'
                ],
                "Zentra": [
                    'Battery Percent', 'Battery Voltage', 'battery', 'Battery',
                    'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct'
                ],
                "Allmeteo": [
                    'battery', 'Battery', 'Battery Voltage', 'Battery Percent',
                    'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct'
                ],
                "OTT": [
                    'battery', 'Battery', 'Battery Voltage', 'Battery Percent',
                    'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct'
                ],
                "Sutron": [
                    'battery', 'Battery', 'Battery Voltage', 'Battery Percent',
                    'batt', 'batt_v', 'batt_volt', 'batt_percent', 'battery_level', 'battLevel', 'battVolt', 'battPct'
                ],
            }

            # Initialize default values
            battery_status = "Unknown"
            connectivity_status = "Unknown"
            
            if rounded_hour in measurements_by_hour:
                # --- Battery status: check all possible fields ---
                battery_fields = battery_fields_by_brand.get(brand_name, ['battery', 'Battery'])
                battery_values = []
                for field in battery_fields:
                    if field in measurements_by_hour[rounded_hour]:
                        battery_reading = min(measurements_by_hour[rounded_hour][field], 
                                              key=lambda x: abs(x['timestamp'] - rounded_hour))
                        battery_values.append(f"{field}: {battery_reading['value']}")
                if battery_values:
                    battery_status = ", ".join(battery_values)
                else:
                    # Debug: log available fields if battery is unknown
                    available_fields = list(measurements_by_hour[rounded_hour].keys())
                    logger.warning(f"No battery field found for station {station_id} at {rounded_hour} (brand: {brand_name}). Available fields: {available_fields}")

                # --- Connectivity status (3D_Paws only, as before) ---
                if brand_name == "3D_Paws" and 'css' in measurements_by_hour[rounded_hour]:
                    css_reading = min(measurements_by_hour[rounded_hour]['css'], 
                                      key=lambda x: abs(x['timestamp'] - rounded_hour))
                    css_value = css_reading['value']
                    connectivity_status = self.get_connectivity_status(css_value)
                elif brand_name == "OTT":
                    # For OTT stations, determine connectivity based on data freshness
                    # If we have recent battery data, consider it connected
                    if battery_status != "Unknown":
                        connectivity_status = "Connected"
                    else:
                        connectivity_status = "No Data"
                elif brand_name in ["Allmeteo", "Zentra"]:
                    # For Allmeteo and Zentra stations, determine connectivity based on data freshness
                    # If we have recent battery data, consider it connected
                    if battery_status != "Unknown":
                        connectivity_status = "Connected"
                    else:
                        connectivity_status = "No Data"
                elif brand_name == "Sutron":
                    # For Sutron stations, determine connectivity based on data freshness
                    # If we have recent battery data, consider it connected
                    if battery_status != "Unknown":
                        connectivity_status = "Connected"
                    else:
                        connectivity_status = "No Data"
            else:
                # No measurements for this hour, but still create health log
                logger.info(f"No measurements for station {station_id} at {rounded_hour}, creating health log with default values")
                
                # For OTT stations, try to get battery status from recent data
                if brand_name == "OTT":
                    try:
                        from database.models import Measurement
                        from django.utils import timezone
                        from datetime import timedelta
                        
                        # Look for recent battery measurements (within last 24 hours)
                        one_day_ago = timezone.now() - timedelta(days=1)
                        recent_battery = Measurement.objects.filter(
                            station_id=station_id,
                            sensor__type='Battery',
                            date__gte=one_day_ago.date()
                        ).order_by('-date', '-time').first()
                        
                        if recent_battery:
                            battery_value = float(recent_battery.value)
                            if battery_value >= 80:
                                battery_status = "Excellent"
                            elif battery_value >= 60:
                                battery_status = "Good"
                            elif battery_value >= 40:
                                battery_status = "Fair"
                            elif battery_value >= 20:
                                battery_status = "Poor"
                            else:
                                battery_status = "Critical"
                            
                            connectivity_status = "Connected"
                            logger.info(f"OTT station {station_id}: Found recent battery data {battery_value}%, status: {battery_status}")
                    except Exception as e:
                        logger.warning(f"Error getting recent battery data for OTT station {station_id}: {e}")

            # Create health log entry
            StationHealthLog.objects.create(
                station_id=station_id,
                battery_status=battery_status,
                connectivity_status=connectivity_status,
                created_at=rounded_hour
            )

        except Exception as e:
            logger.error(f"Error processing station health: {e}")
            self.stdout.write(self.style.ERROR(f"Error processing station health: {e}"))

    def get_connectivity_status(self, css_value):
        """Convert CSS value to connectivity status"""
        try:
            css_value = float(css_value)
            if css_value >= -70:
                return "Excellent"
            elif css_value >= -85:
                return "Good"
            elif css_value >= -100:
                return "Fair"
            else:
                return "Poor"
        except (TypeError, ValueError):
            return "Unknown"

    def get_sensor_id(self, sensor_type):
        """Get sensor ID from the database"""
        try:
            sensor = Sensor.objects.get(type=sensor_type)
            return sensor.id
        except Sensor.DoesNotExist:
            return None

    def round_to_nearest_hour(self, timestamp_str):
        """Rounds the given timestamp to the nearest hour"""
        timestamp = parse_datetime(timestamp_str)
        if timestamp.minute >= 30:
            timestamp = timestamp.replace(minute=0) + timedelta(hours=1)
        else:
            timestamp = timestamp.replace(minute=0)
        return timestamp.replace(second=0, microsecond=0)

    def get_closest_measurement(self, entries, rounded_hour):
        """Find the closest measurement to the rounded hour"""
        closest_entry = None
        closest_time_diff = None
        for entry in entries:
            timestamp = parse_datetime(entry["time"])
            time_diff = abs(timestamp - rounded_hour)
            if closest_time_diff is None or time_diff < closest_time_diff:
                closest_time_diff = time_diff
                closest_entry = entry
        return closest_entry

    def parse_datetime(self, datetime_str):
        """Parse datetime string to Trinidad and Tobago timezone (UTC-4)"""
        tt_tz = timezone.get_fixed_timezone(-240)
        
        if isinstance(datetime_str, str):
            try:
                parsed_datetime = parser.parse(datetime_str)
                if parsed_datetime.tzinfo is None:
                    parsed_datetime = timezone.make_aware(parsed_datetime, tt_tz)
                return parsed_datetime.astimezone(tt_tz)
            except ValueError:
                logger.warning("Invalid datetime format: %s", datetime_str)
                return None
        elif isinstance(datetime_str, (int, float)):
            try:
                if datetime_str < 0 or datetime_str > 32503680000:
                    logger.warning("Invalid Unix timestamp value: %s", datetime_str)
                    return None
                timestamp = datetime.utcfromtimestamp(datetime_str)
                return timezone.make_aware(timestamp, tt_tz)
            except (ValueError, OSError) as e:
                logger.warning("Invalid Unix timestamp value: %s (%s)", datetime_str, e)
                return None
        else:
            logger.warning("Invalid datetime value: %s", datetime_str)
            return None

    def ensure_historical_station_sensor_relationships(self, connection, stations, sensors):
        """Ensure all historical station-sensor relationships are established for the last 3 months"""
        try:
            self.stdout.write("Ensuring all historical station-sensor relationships are established...")
            
            # Get all unique sensor types that have been used in the last 3 months
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT SENSORNAME as sensor_name
                FROM xc_data1 d
                JOIN xc_sites s ON d.STATION_ID = s.STATION_ID
                WHERE d.TIME_TAG > DATE_SUB(NOW(), INTERVAL 3 MONTH) 
                AND s.ENABLED = 'Y'
                ORDER BY SENSORNAME
            """)
            historical_sensors = cursor.fetchall()
            cursor.close()
            
            self.stdout.write(f"Found {len(historical_sensors)} sensors with data in the last 3 months")
            
            # Ensure all these sensors exist in our local database
            for sensor_row in historical_sensors:
                sensor_name = sensor_row['sensor_name']
                if sensor_name not in sensors:
                    units = self.get_sensor_unit(sensor_name)
                    sensor, created = Sensor.objects.get_or_create(
                        type=sensor_name,
                        defaults={'unit': units}
                    )
                    sensors[sensor_name] = sensor
                    if created:
                        self.stdout.write(f"Created missing historical sensor: {sensor_name}")
            
            # Now establish relationships for all stations with all historical sensors
            for station_id, station in stations.items():
                historical_sensor_types = [s['sensor_name'] for s in historical_sensors]
                self.pre_create_station_sensor_relationships(station.id, historical_sensor_types)
                self.stdout.write(f"Established historical relationships for station {station.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error ensuring historical station-sensor relationships: {e}")
            return False