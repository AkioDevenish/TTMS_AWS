from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Brand, Station, Sensor, Measurement,
    StationHealthLog, StationSensor, ApiAccessKey,
    SystemLog, User, Notification, Message, Chat, UserPresence, Bill, TaskExecution, ApiKeyUsageLog
)
from .serializers import (
    BrandSerializer, StationSerializer, SensorSerializer,
    MeasurementSerializer, StationSerializer, StationHealthLogSerializer,
    StationSensorSerializer, ApiAccessKeySerializer, SystemLogSerializer,
    UserSerializer, NotificationSerializer, MessageSerializer,
    UserCreateSerializer, LoginSerializer, ChatSerializer, UserPresenceSerializer,
    BillSerializer, ApiKeyUsageLogSerializer
)
from django.utils import timezone
from rest_framework import serializers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime, timedelta, timezone as tz
from django.db.models import Q
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from django.http import HttpResponse
import logging
from rest_framework.pagination import PageNumberPagination
import math
import time
from django.db.models import Subquery, OuterRef
from django.core.management.base import BaseCommand
from django.db.models import Window, F
from django.db.models.functions import RowNumber
from django.db.models import Max
import uuid
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from .auth import ApiKeyAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from .renderers import MeasurementCSVRenderer, StationCSVRenderer
from django.core.cache import cache
from django.db import models
from django.db.models import Prefetch

User = get_user_model()
logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @action(detail=True, methods=['get'])
    def stations(self, request, pk=None):
        brand = self.get_object()
        stations = brand.stations.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    renderer_classes = [JSONRenderer, XMLRenderer, StationCSVRenderer]

    def list(self, request, *args, **kwargs):
        """Override list to include additional filtering options."""
        queryset = self.get_queryset()
        
        # Filter by brand if provided
        brand = request.query_params.get('brand')
        if brand:
            # Try both brand relationship patterns
            try_brand_relation = queryset.filter(brand__name=brand)
            if try_brand_relation.exists():
                queryset = try_brand_relation
            else:
                queryset = queryset.filter(brand_name=brand)
        
        # No pagination to ensure all stations are returned
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            print("Received data:", request.data)
            data = request.data.copy()
            if 'last_updated_at' not in data:
                data['last_updated_at'] = timezone.now()

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def measurements(self, request, pk=None):
        station = self.get_object()
        measurements = station.measurements.all()
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def health_logs(self, request, pk=None):
        station = self.get_object()
        logs = station.health_logs.all()
        serializer = StationHealthLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def latest_health(self, request, pk=None):
        station = self.get_object()
        latest_health = station.health_logs.order_by('-created_at').first()
        if latest_health:
            serializer = StationHealthLogSerializer(latest_health)
            return Response(serializer.data)
        return Response({'error': 'No health data available'}, status=404)


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @action(detail=True, methods=['get'])
    def stations(self, request, pk=None):
        sensor = self.get_object()
        stations = sensor.stations.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)


class MeasurementPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    pagination_class = MeasurementPagination
    renderer_classes = [JSONRenderer, XMLRenderer, MeasurementCSVRenderer]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def by_station(self, request):
        """Get measurements for a specific station with optimized performance."""
        station_id = request.query_params.get('station_id')
        if not station_id:
            return Response({"error": "station_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get query parameters for filtering
            sensor_type = request.query_params.get('sensor_type')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            limit = request.query_params.get('limit')
            
            # Start with optimized station filtering
            measurements = self.queryset.filter(station_id=station_id)
            
            # Apply additional filters if provided
            if sensor_type:
                # Try both direct type filter and sensor relationship
                try:
                    # First try with sensor relationship
                    measurements = measurements.filter(sensor__type=sensor_type)
                except:
                    # If that fails, try with sensor_type field if it exists
                    if hasattr(Measurement, 'sensor_type'):
                        measurements = measurements.filter(sensor_type=sensor_type)
            
            if start_date:
                measurements = measurements.filter(date__gte=start_date)
            
            if end_date:
                measurements = measurements.filter(date__lte=end_date)
            
            # Order by date and time (newest first)
            measurements = measurements.order_by('-date', '-time')
            
            # Apply limit if provided
            if limit and limit.isdigit():
                measurements = measurements[:int(limit)]
            
            serializer = self.serializer_class(measurements, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            import traceback
            print(f"Error in by_station: {str(e)}")
            print(traceback.format_exc())
            
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_sensor(self, request):
        sensor_id = request.query_params.get('sensor_id')
        if not sensor_id:
            return Response({"error": "sensor_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        measurements = self.queryset.filter(sensor_id=sensor_id)
        serializer = self.serializer_class(measurements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def highest_by_brand(self, request):
        """Get highest measurements for each sensor at each station by brand name."""
        brand = request.query_params.get('brand')
        if not brand:
            return Response({"error": "brand parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Debug information
            print(f"Looking for highest measurements for brand: {brand}")
            
            # Get stations for this brand (trying both relationship patterns)
            stations = Station.objects.filter(brand__name=brand)
            if not stations.exists():
                # Try direct field if relationship doesn't work
                stations = Station.objects.filter(brand_name=brand)
                
            if not stations.exists():
                print(f"No stations found for brand: {brand}")
                return Response([], status=status.HTTP_200_OK)
            
            station_ids = list(stations.values_list('id', flat=True))
            print(f"Found {len(station_ids)} stations for brand {brand}: {station_ids}")
            
            result = []
            
            # For each station, find the highest value for each sensor
            for station in stations:
                # Get sensors for this station
                station_sensors = StationSensor.objects.filter(station_id=station.id)
                sensor_ids = station_sensors.values_list('sensor_id', flat=True).distinct()
                sensors = Sensor.objects.filter(id__in=sensor_ids)
                
                # Get measurements for this station
                station_measurements = Measurement.objects.filter(station_id=station.id)
                
                # For each sensor, find the highest measurement
                for sensor in sensors:
                    sensor_measurements = station_measurements.filter(sensor_id=sensor.id)
                    if not sensor_measurements.exists():
                        continue
                        
                    highest = sensor_measurements.order_by('-value').first()
                    if highest:
                        result.append({
                            'station_name': station.name,
                            'brand_name': brand,
                            'date': highest.date,
                            'time': highest.time,
                            'value': highest.value,
                            'sensor_type': sensor.type,
                            'sensor_unit': sensor.unit
                        })
            
            print(f"Found {len(result)} highest measurements")
            return Response(result)
        
        except Exception as e:
            import traceback
            print(f"Error in highest_by_brand: {str(e)}")
            print(traceback.format_exc())
            
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def latest_by_station(self, request):
        """Get latest measurements for each sensor at each station by brand name."""
        try:
            # Get the brand name from the request parameters
            brand = request.query_params.get('brand')
            sensor_type = request.query_params.get('sensor_type')
            
            if not brand:
                return Response(
                    {"error": "Brand parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            print(f"Getting latest measurements for brand {brand}")
            
            # Get stations by brand
            stations = Station.objects.filter(brand__name=brand)
            print(f"Found {stations.count()} stations for brand {brand}")
            
            # Filter query if sensor_type is provided
            sensor_filter = {'type': sensor_type} if sensor_type else {}
            sensors = Sensor.objects.filter(**sensor_filter)
            
            # Prepare the response data
            result = []
            
            # For each station, find the latest measurement for each sensor
            for station in stations:
                station_sensors = StationSensor.objects.filter(station_id=station.id)
                sensor_ids = station_sensors.values_list('sensor_id', flat=True).distinct()
                
                if sensor_type:
                    station_sensors = station_sensors.filter(sensor__type=sensor_type)
                
                for sensor in sensors.filter(id__in=sensor_ids):
                    # Get the latest measurement for this station and sensor
                    latest = Measurement.objects.filter(
                        station_id=station.id,
                        sensor_id=sensor.id
                    ).order_by('-date', '-time').first()
                    
                    if latest:
                        result.append({
                            'station_id': station.id,
                            'station_name': station.name,
                            'brand_name': brand,
                            'date': latest.date,
                            'time': latest.time,
                            'value': latest.value,
                            'sensor_type': sensor.type,
                            'sensor_unit': sensor.unit
                        })
            
            print(f"Found {len(result)} latest measurements")
            return Response(result)
            
        except Exception as e:
            import traceback
            print(f"Error in latest_by_station: {str(e)}")
            print(traceback.format_exc())
            
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def recent_by_brand(self, request):
        """Get recent measurements (last 12 hours) for each sensor at each station by brand name."""
        try:
            # Get the brand name from the request parameters
            brand = request.query_params.get('brand')
            sensor_type = request.query_params.get('sensor_type')
            hours = int(request.query_params.get('hours', 12))  # Default to 12 hours
            
            if not brand:
                return Response(
                    {"error": "Brand parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            print(f"Getting recent measurements for brand {brand}, last {hours} hours")
            
            # Calculate the time threshold
            time_threshold = timezone.now() - timezone.timedelta(hours=hours)
            
            # Get stations by brand
            stations = Station.objects.filter(brand_name=brand)
            print(f"Found {stations.count()} stations for brand {brand}")
            
            # If no stations found, return empty result
            if not stations.exists():
                return Response([])
            
            # Prepare the response data
            result = []
            
            # For each station, find recent measurements
            for station in stations:
                # Base query for measurements
                measurements_query = Measurement.objects.filter(
                    station_id=station.id,
                    date_time__gte=time_threshold
                ).order_by('-date_time')
                
                # Apply sensor type filter if provided
                if sensor_type:
                    measurements_query = measurements_query.filter(sensor_type=sensor_type)
                
                # Get measurements
                measurements = measurements_query[:50]  # Limit to 50 most recent
                
                # Add each measurement to the result
                for m in measurements:
                    result.append({
                        'station_id': station.id,
                        'station_name': station.name,
                        'brand_name': brand,
                        'date': m.date,
                        'time': m.time,
                        'date_time': m.date_time.isoformat() if m.date_time else f"{m.date}T{m.time}",
                        'value': m.value,
                        'sensor_type': m.sensor_type,
                        'sensor_unit': m.unit
                    })
            
            print(f"Found {len(result)} recent measurements")
            return Response(result)
            
        except Exception as e:
            import traceback
            print(f"Error in recent_by_brand: {str(e)}")
            print(traceback.format_exc())
            
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def measurements_by_brand(self, request):
        """Get time series measurements (last 12 hours) for each station by brand."""
        try:
            # Get parameters
            brand = request.query_params.get('brand')
            sensor_type = request.query_params.get('sensor_type')
            hours = int(request.query_params.get('hours', 12))
            
            if not brand:
                return Response({"error": "Brand parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"Getting time series data for brand: {brand}, sensor: {sensor_type}, hours: {hours}")
            
            # Calculate time threshold (12 hours ago by default)
            time_threshold = timezone.now() - timezone.timedelta(hours=hours)
            
            # Find stations for this brand
            stations = Station.objects.filter(brand_name=brand)
            print(f"Found {stations.count()} stations for brand {brand}")
            
            if not stations.exists():
                return Response([])
            
            result = []
            
            # For each station, get recent measurements
            for station in stations:
                # Query for measurements
                query = Measurement.objects.filter(
                    station_id=station.id,
                    date_time__gte=time_threshold
                ).order_by('date_time')  # Chronological order
                
                # Apply sensor type filter if provided
                if sensor_type:
                    query = query.filter(sensor_type=sensor_type)
                
                # Get measurements
                measurements = list(query)
                print(f"Found {len(measurements)} measurements for station {station.name}")
                
                # Add each measurement to the result
                for m in measurements:
                    result.append({
                        'station_id': station.id,
                        'station_name': station.name,
                        'brand_name': brand,
                        'date': m.date,
                        'time': m.time,
                        'date_time': m.date_time.isoformat() if m.date_time else f"{m.date}T{m.time}",
                        'value': m.value,
                        'sensor_type': m.sensor_type,
                        'sensor_unit': m.unit
                    })
            
            print(f"Returning {len(result)} total measurements across all stations")
            return Response(result)
            
        except Exception as e:
            import traceback
            print(f"Error in measurements_by_brand: {str(e)}")
            print(traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def station_overview(self, request):
        try:
            # Get query parameters
            brand = request.GET.get('brand')
            sensor_type = request.GET.get('sensor_type')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            latest = request.GET.get('latest', 'true').lower() == 'true'

            # Create cache key
            cache_key = f'station_overview_{brand}_{sensor_type}_{page}_{page_size}_{latest}'
            cached_data = cache.get(cache_key)
            
            if cached_data:
                return Response(cached_data)

            # Get current time and 12 hours ago
            now = timezone.now()
            yesterday = now - timedelta(hours=12)
            
            # Base queryset with select_related and prefetch_related
            stations = Station.objects.filter(
                brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT']
            ).select_related('brand').prefetch_related(
                Prefetch(
                    'measurements',
                    queryset=Measurement.objects.filter(
                        sensor__type=sensor_type,
                        date__gte=yesterday.date()
                    ).order_by('-date', '-time')
                )
            )

            if brand:
                stations = stations.filter(brand__name=brand)

            # Get total count for pagination
            total_count = stations.count()
            total_pages = (total_count + page_size - 1) // page_size

            # Apply pagination
            start = (page - 1) * page_size
            end = start + page_size
            stations = stations[start:end]

            # Process stations data
            response_data = []
            for station in stations:
                latest_measurement = station.measurements.first() if station.measurements.exists() else None
                
                station_data = {
                    'id': station.id,
                    'name': station.name,
                    'address': station.address,
                    'brand': station.brand.name,
                    'sensor_unit': self.get_sensor_unit(sensor_type),
                    'latest_measurement': {
                        'value': float(latest_measurement.value) if latest_measurement else None,
                        'date': latest_measurement.date.isoformat() if latest_measurement else None,
                        'time': latest_measurement.time.isoformat() if latest_measurement else None,
                        'status': latest_measurement.status if latest_measurement else 'No Data'
                    } if latest_measurement else None
                }
                response_data.append(station_data)

            result = {
                'stations': response_data,
                'total': total_count,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages
            }

            # Cache the result for 5 minutes
            cache.set(cache_key, result, timeout=300)
            
            return Response(result)

        except Exception as e:
            import traceback
            print(f"Error in station_overview: {str(e)}")
            print(traceback.format_exc())
            return Response({
                'stations': [],
                'total': 0,
                'page': 1,
                'page_size': page_size,
                'error': str(e)
            })

    def get_sensor_unit(self, sensor_type):
        """Helper function to get the unit for a sensor type"""
        sensor_units = {
            'bt1': '°C',
            'mt1': '°C',
            'bp1': 'hPa',
            'ws': 'm/s',
            'wd': '°',
            'rg': 'mm',
            'sv1': 'W/m²',
            'si1': 'W/m²',
            'su1': 'W/m²',
            'bpc': '%',
            'css': '%',
            'Air Temperature': '°C',
            'Wind Speed': 'm/s',
            'Precipitation': 'mm',
            'Solar Radiation': 'W/m²',
            'Relative Humidity': '%',
            'Atmospheric Pressure': 'kPa',
            'wind_ave10': 'm/s',
            'dir_ave10': '°',
            'battery': 'V'
        }
        return sensor_units.get(sensor_type, '')

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get historical measurements for specific stations and sensor type(s).
        Query parameters:
        - station_ids: Comma-separated list of station IDs
        - sensor_type: Comma-separated list of sensor types (e.g., bt1,rg,ws)
        - hours: Number of hours to look back (default: 12)
        """
        try:
            print("History endpoint called with params:", request.query_params)
            station_ids_param = request.query_params.get('station_ids', '')
            sensor_type_param = request.query_params.get('sensor_type')
            hours = int(request.query_params.get('hours', 12))
            print(f"Parsed parameters: station_ids={station_ids_param}, sensor_type={sensor_type_param}, hours={hours}")
            if not station_ids_param or not sensor_type_param:
                print("Missing required parameters")
                return Response(
                    {"detail": "station_ids and sensor_type parameters are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                station_ids = [int(id) for id in station_ids_param.split(',')]
                print(f"Parsed station IDs: {station_ids}")
            except ValueError:
                print("Invalid station_ids format")
                return Response(
                    {"detail": "Invalid station_ids format. Use comma-separated integers"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Support multiple sensor types
            sensor_types = [s.strip() for s in sensor_type_param.split(',') if s.strip()]
            if not sensor_types:
                print("No valid sensor types provided")
                return Response(
                    {"detail": "At least one sensor_type must be provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            now = timezone.now()
            time_threshold = now - timedelta(hours=hours)
            threshold_date = time_threshold.date()
            threshold_time = time_threshold.time()
            print(f"Time threshold: {threshold_date} {threshold_time}")
            measurements = Measurement.objects.filter(
                station_id__in=station_ids,
                sensor__type__in=sensor_types
            ).filter(
                (Q(date=threshold_date) & Q(time__gte=threshold_time)) | 
                (Q(date__gt=threshold_date))
            ).order_by('station_id', 'sensor__type', 'date', 'time')
            print(f"Found {measurements.count()} measurements")
            result_data = []
            for m in measurements:
                result_data.append({
                    'station_id': m.station_id,
                    'sensor_type': m.sensor.type,
                    'value': m.value,
                    'date': m.date.strftime('%Y-%m-%d'),
                    'time': m.time.strftime('%H:%M:%S')
                })

            # Insert into api_key_usage logs and update Api_Access_Keys
            print(f"Checking request.auth type: {type(request.auth)}") # Debug print
            if request.auth and isinstance(request.auth, ApiAccessKey):
                print("API key authenticated, attempting to log usage.") # Debug print
                try:
                    api_key = request.auth
                    user = api_key.user

                    # Update last_used timestamp
                    api_key.last_used = timezone.now()
                    api_key.save(update_fields=['last_used'])

                    # Create usage log entry
                    log_data = {
                        'api_key': api_key,
                        'user': user,
                        'request_path': request.path,
                        'query_params': dict(request.query_params),
                        'response_format': request.accepted_renderer.format,
                        'status_code': 200,
                        'user_agent': request.META.get('HTTP_USER_AGENT', '')
                    }
                    print(f"Attempting to create ApiKeyUsageLog with data: {log_data}") # Debug print log data
                    ApiKeyUsageLog.objects.create(**log_data)
                    print("ApiKeyUsageLog created successfully.") # Debug print success

                except Exception as e:
                    # Log the specific error during log creation
                    print(f"SPECIFIC Error logging API key usage: {type(e).__name__} - {str(e)}") # More specific error logging
                    # Don't fail the request if logging fails

            return Response({'measurements': result_data})
        except Exception as e:
            import traceback
            print(f"Error in history endpoint: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# 

class HistoricalDataViewSet(viewsets.ViewSet):
    """ViewSet for retrieving historical measurement data."""
    authentication_classes = [ApiKeyAuthentication, JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, XMLRenderer, MeasurementCSVRenderer]
    
    @action(detail=False, methods=['get'], url_path='get_readings')
    def get_readings(self, request, format=None):
        """Get historical measurements for a specific station."""
        station_id = request.query_params.get('station_id')
        if not station_id:
            return Response({"error": "station_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get query parameters for filtering
            sensor_types = request.query_params.get('sensor_type', '').split(',')
            
            # Calculate default time range (last 12 hours)
            now = timezone.now()
            default_start = now - timedelta(hours=12)
            
            # Get start_date and end_date from params or use defaults
            start_date = request.query_params.get('start_date', default_start.date().isoformat())
            end_date = request.query_params.get('end_date', now.date().isoformat())
            
            # If using default start_date, also consider the time
            if start_date == default_start.date().isoformat():
                measurements = Measurement.objects.filter(
                    station_id=station_id,
                    date__gte=default_start.date(),
                    time__gte=default_start.time()
                )
            else:
                measurements = Measurement.objects.filter(station_id=station_id)
                measurements = measurements.filter(date__gte=start_date)
                if end_date:
                    measurements = measurements.filter(date__lte=end_date)
            
            # Apply sensor type filter
            if sensor_types and sensor_types[0]:  # Check if there are sensor types
                measurements = measurements.filter(sensor__type__in=sensor_types)
            
            # Order by sensor type, date and time (newest first)
            measurements = measurements.order_by('sensor__type', '-date', '-time')
            
            # Apply limit if provided
            limit = request.query_params.get('limit')
            if limit and limit.isdigit():
                measurements = measurements[:int(limit)]
            
            # Use MeasurementSerializer with specific fields
            serializer = MeasurementSerializer(
                measurements, 
                many=True,
                fields=['station_name', 'sensor_type', 'date', 'time', 'value']
            )
            
            # Group data by sensor type
            grouped_data = []
            for measurement in serializer.data:
                grouped_data.append({
                 
                    'station_name': measurement['station_name'],
                    'sensor_type': measurement['sensor_type'],
                    'date': measurement['date'],
                    'time': measurement['time'],
                    'value': measurement['value']
                })
            
            # Insert into api_key_usage logs and update Api_Access_Keys
            print(f"Checking request.auth type: {type(request.auth)}") # Debug print
            if request.auth and isinstance(request.auth, ApiAccessKey):
                print("API key authenticated, attempting to log usage.") # Debug print
                try:
                    api_key = request.auth
                    user = api_key.user
                    
                    # Update last_used timestamp
                    api_key.last_used = timezone.now()
                    api_key.save(update_fields=['last_used'])
                    
                    # Create usage log entry
                    log_data = {
                        'api_key': api_key,
                        'user': user,
                        'request_path': request.path,
                        'query_params': dict(request.query_params),
                        'response_format': request.accepted_renderer.format,
                        'status_code': 200,
                        'user_agent': request.META.get('HTTP_USER_AGENT', '')
                    }
                    print(f"Attempting to create ApiKeyUsageLog with data: {log_data}") # Debug print log data
                    ApiKeyUsageLog.objects.create(**log_data)
                    print("ApiKeyUsageLog created successfully.") # Debug print success

                except Exception as e:
                    # Log the specific error during log creation
                    print(f"SPECIFIC Error logging API key usage: {type(e).__name__} - {str(e)}") # More specific error logging
                    # Don't fail the request if logging fails
            
            # Check if CSV format is requested
            if request.accepted_renderer.format == 'csv':
                # For CSV, return flat list directly
                return Response(grouped_data)
            else:
                # For JSON/XML, keep your nested structure
                return Response({
                    'data': grouped_data
                })
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StationHealthLogViewSet(viewsets.ModelViewSet):
    queryset = StationHealthLog.objects.all()
    serializer_class = StationHealthLogSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Get the latest health log for each station using a more efficient query
        latest_logs = (
            StationHealthLog.objects
            .values('station')
            .annotate(max_id=models.Max('id'))
            .values('max_id')
        )
        
        # Get the actual logs with related station data
        queryset = (
            StationHealthLog.objects
            .filter(id__in=latest_logs)
            .select_related('station')
            .order_by('station__name')
        )
        
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            # If station ID is provided, get the station
            station_id = request.data.get('station')
            if not station_id:
                return Response(
                    {"error": "Station ID is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the health log
            health_log = StationHealthLog.objects.create(
                station_id=station_id,
                battery_status=request.data.get('battery_status', 'Unknown'),
                connectivity_status=request.data.get('connectivity_status', 'No Data'),
                created_at=timezone.now()
            )

            serializer = self.get_serializer(health_log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class StationSensorViewSet(viewsets.ModelViewSet):
    queryset = StationSensor.objects.all()
    serializer_class = StationSensorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        station_id = request.query_params.get('station_id')
        brand = request.query_params.get('brand')

        if station_id:
            queryset = queryset.filter(station_id=station_id)
        if brand:
            queryset = queryset.filter(station__brand__name=brand)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ApiAccessKeyViewSet(viewsets.ModelViewSet):
    queryset = ApiAccessKey.objects.all()
    serializer_class = ApiAccessKeySerializer


class SystemLogViewSet(viewsets.ModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'])
    def by_module(self, request):
        module = request.query_params.get('module')
        if not module:
            return Response({"error": "module is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.queryset.filter(module=module)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]  # Only admins can update/delete
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Prevent deleting yourself
            if instance.id == request.user.id:
                return Response(
                    {"error": "You cannot delete your own account"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Only superusers can delete other users
            if not request.user.is_superuser:
                return Response(
                    {"error": "Only superusers can delete users"},
                    status=status.HTTP_403_FORBIDDEN
                )
            self.perform_destroy(instance)
            return Response(
                {"message": "User deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Validate expires_at format
        if 'expires_at' in data and data['expires_at']:
            try:
                # Parse the date and set it to end of day in UTC
                date = datetime.strptime(data['expires_at'], '%Y-%m-%d')
                date = date.replace(hour=23, minute=59, second=59)
                # Convert to UTC timezone-aware datetime
                data['expires_at'] = timezone.make_aware(date, tz.utc)
            except ValueError:
                return Response(
                    {"error": "Invalid date format for expires_at. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate API key for newly created active users
            if user.status == 'Active':
                try:
                    api_key = self.generate_api_key(user)
                    logger.info(f"API key {api_key.uuid} created for new user {user.email}")
                except Exception as e:
                    logger.error(f"Failed to create API key for new user {user.email}: {str(e)}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        original_status = instance.status
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        
        # Check if status changed from non-Active to Active
        if original_status != 'Active' and updated_user.status == 'Active':
            try:
                api_key = self.generate_api_key(updated_user)
                logger.info(f"API key {api_key.uuid} created for activated user {updated_user.email}")
                
                # Create a system log entry
                SystemLog.objects.create(
                    module="User Management",
                    activity=f"API key automatically generated for user {updated_user.email}",
                    type="API Key Generation",
                    user_id=updated_user.id
                )
            except Exception as e:
                logger.error(f"Failed to create API key for activated user {updated_user.email}: {str(e)}")
        
        return Response(serializer.data)

    def generate_api_key(self, user):
        """Generate a new API key for a user"""
        try:
            # Generate a new UUID for the API key
            api_key_uuid = uuid.uuid4()
            
            # Use the user's expiration date for the API key
            expires_at = user.expires_at
            
            # Create the API key record
            api_key = ApiAccessKey.objects.create(
                uuid=api_key_uuid,
                token_name=f"Default Key for {user.email}",
                user=user,
                expires_at=expires_at,
                note="Automatically generated on account activation"
            )
            
            # Create system log entry
            SystemLog.objects.create(
                module="User Management",
                activity=f"API key automatically generated for user {user.email}",
                type="API Key Generation",
                user_id=user.id
            )
            
            # Send email notification to the user
            email_sent = self._send_api_key_email(user, api_key)
            if not email_sent:
                logger.warning(f"API key created for {user.email} but email notification failed")
            
            return api_key
        
        except Exception as e:
            logger.error(f"Error generating API key for user {user.email}: {str(e)}")
            raise

    @action(detail=True, methods=['get', 'post'])
    def presence(self, request, pk=None):
        if request.method == 'POST':
            if int(pk) != request.user.id:
                return Response(
                    {"error": "Cannot update other user's presence"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            try:
                user_presence, _ = UserPresence.objects.get_or_create(user_id=pk)
                user_presence.is_online = request.data.get('is_online', False)
                user_presence.save()
                
                return Response({
                    'id': pk,
                    'is_online': user_presence.is_online,
                    'last_seen': user_presence.last_seen
                })
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:  # GET request
            presences = UserPresence.objects.all()
            serializer = UserPresenceSerializer(presences, many=True)
            return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # If status is being updated
            if 'status' in request.data:
                # Only superusers can change status
                if not request.user.is_superuser:
                    return Response(
                        {"error": "Only administrators can modify user status"},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Prevent self-suspension
                if instance.id == request.user.id:
                    return Response(
                        {"error": "You cannot modify your own status"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Update the status
                new_status = request.data['status']
                if new_status not in [choice[0] for choice in User.STATUS_CHOICES]:
                    return Response(
                        {"error": "Invalid status value"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                instance.status = new_status
                instance.save(update_fields=['status'])
                
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            
            return Response(
                {"error": "No status provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _send_api_key_email(self, user, api_key):
        """Send email notification about the generated API key to the user"""
        try:
            logger.info(f"Sending API key email to {user.email}")
            
            subject = f"Your API Key for {settings.SITE_NAME}"
            
            # Create a message with API key details
            message = f"""
Hello {user.first_name},

Your account has been activated, and an API key has been generated for you.

API Key Details:
----------------
Key ID: {api_key.uuid}
Name: {api_key.token_name}
Expires: {api_key.expires_at.strftime('%Y-%m-%d %H:%M:%S')}

Keep this key secure and do not share it with others. This key allows access to our API services.

To use your API key, include it in the Authorization header of your requests:
Authorization: Bearer {api_key.uuid}

If you have any questions, please contact our support team.

Best regards,
The {settings.SITE_NAME} Team
"""
            
            # Send the email
            sent = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            if sent:
                logger.info(f"API key email successfully sent to {user.email}")
                
                # Create a system log entry for the email sent
                SystemLog.objects.create(
                    module="User Management",
                    activity=f"API key email sent to user {user.email}",
                    type="Email Notification",
                    user_id=user.id
                )
                return True
            else:
                logger.error(f"Failed to send API key email to {user.email}")
                return False
            
        except Exception as e:
            logger.error(f"Error sending API key email to {user.email}: {str(e)}")
            return False


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=False, methods=['get'])
    def unread(self, request):
        notifications = self.queryset.filter(read_at__isnull=True)
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read_at = timezone.now()
        notification.save()
        serializer = self.serializer_class(notification)
        return Response(serializer.data)

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'stations', StationViewSet)
router.register(r'station-health-logs', StationHealthLogViewSet)
router.register(r'station-sensors', StationSensorViewSet)
router.register(r'api-tokens', ApiAccessKeyViewSet)
router.register(r'system-logs', SystemLogViewSet)
router.register(r'users', UserViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    return Response({'valid': True})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_user(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        })
    return Response({'detail': 'Not authenticated'}, status=401)

@api_view(['GET'])
def get_latest_timestamp(request):
    latest_measurement = Measurement.objects.order_by('-date', '-time').first()
    if latest_measurement:
        timestamp = f"{latest_measurement.date}T{latest_measurement.time}"
        return Response({'timestamp': timestamp})
    return Response({'timestamp': None}, status=404)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user = serializer.validated_data['user']
            
            # Check user status
            if user.status == 'Suspended':
                return Response(
                    {'error': 'Your account has been suspended. Please contact support.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            elif user.status == 'Inactive':
                return Response(
                    {'error': 'Your account has expired. Please renew your subscription.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Generate tokens
            try:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'role': user.role,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                        'status': user.status
                    }
                })
            except Exception as token_error:
                print(f"Token generation error: {str(token_error)}")
                return Response(
                    {'error': 'Error generating authentication tokens'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            print(f"Login error: {str(e)}")
            return Response(
                {'error': 'Authentication service is temporarily unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                return response
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            print(f"Token obtain error: {str(e)}")
            return Response(
                {'error': 'Authentication service is temporarily unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class MessageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            Q(chat__user=self.request.user) | Q(sender=self.request.user)
        ).order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class ConversationList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user = self.kwargs['user_id']
        return Message.objects.filter(
            Q(chat__user_id=other_user, sender=self.request.user) |
            Q(chat__user=self.request.user, sender_id=other_user)
        ).order_by('created_at')

class MarkMessageRead(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.recipient == request.user and not message.read_at:
            message.read_at = timezone.now()
            message.save()
        return Response(self.get_serializer(message).data)

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # If support user, get all users except support
        if self.request.user.email == 'mdpssupport@metoffice.gov.tt':
            return User.objects.exclude(email='mdpssupport@metoffice.gov.tt').order_by('-created_at')
        # For regular users, only get support user
        return User.objects.filter(email='mdpssupport@metoffice.gov.tt')

class ChatListCreate(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # If support user, get all chats
        if user.email == 'mdpssupport@metoffice.gov.tt':
            return Chat.objects.all()\
                .select_related('user')\
                .prefetch_related('messages', 'participants')\
                .order_by('-created_at')
        
        # For regular users, get their chats with support
        return Chat.objects.filter(
            Q(user=user) | 
            Q(participants=user) |
            Q(support_chat=True)
        ).select_related('user')\
         .prefetch_related('messages', 'participants')\
         .order_by('-created_at')

    def perform_create(self, serializer):
        chat = serializer.save(user=self.request.user)
        # Add both users as participants
        chat.participants.add(self.request.user)
        
        # If this is a support chat, add the support user as participant
        if self.request.data.get('support_chat'):
            support_user = User.objects.get(email='mdpssupport@metoffice.gov.tt')
            chat.participants.add(support_user)

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

class ChatMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        return Message.objects.filter(chat_id=chat_id)

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(
            Q(user=self.request.user) | 
            Q(participants=self.request.user)
        ).distinct()

    def create(self, request, *args, **kwargs):
        try:
            print("Creating chat with data:", request.data)
            
            # Check if a chat already exists
            other_user_id = request.data.get('user_id')
            if other_user_id:
                existing_chat = Chat.objects.filter(
                    Q(user=request.user, participants__id=other_user_id) |
                    Q(user_id=other_user_id, participants=request.user)
                ).first()
                
                if existing_chat:
                    print(f"Found existing chat: {existing_chat.id}")
                    return Response(self.get_serializer(existing_chat).data)

            # Create new chat without user in request data
            chat_data = request.data.copy()
            chat_data.pop('user_id', None)  # Remove user_id from data
            
            serializer = self.get_serializer(data=chat_data)
            serializer.is_valid(raise_exception=True)
            
            # Save without committing to add participants
            chat = serializer.save()
            
            # Add participants
            chat.participants.add(request.user)
            if other_user_id:
                chat.participants.add(other_user_id)
            
            print(f"Created new chat: {chat.id}")
            return Response(serializer.data, status=201)
            
        except Exception as e:
            print(f"Error creating chat: {str(e)}")
            return Response({"error": str(e)}, status=400)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            Q(chat__user=self.request.user) | 
            Q(sender=self.request.user)
        ).select_related('sender', 'chat')

    def create(self, request, *args, **kwargs):
        print("Received message data:", request.data)  # Debug print
        
        try:
            chat_id = request.data.get('chat')
            if not chat_id:
                return Response({"error": "Chat ID is required"}, status=400)
                
            chat = get_object_or_404(Chat, id=chat_id)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            message = serializer.save(
                chat=chat,
                sender=request.user,
                time=timezone.now().time()
            )
            
            print(f"Message created: {message.id}")  # Debug print
            return Response(serializer.data, status=201)
            
        except Exception as e:
            print(f"Error creating message: {str(e)}")  # Debug print
            return Response({"error": str(e)}, status=400)

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        
        if self.request.user.is_staff:
            if user_id:
                return Bill.objects.filter(user_id=user_id)
            return Bill.objects.all()
        
        # Regular users can only see their own bills
        return Bill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def verify_receipt(self, request, pk=None):
        if not request.user.is_staff:
            raise PermissionDenied("Only staff can verify receipts")
        
        bill = self.get_object()
        bill.receipt_verified = True
        bill.receipt_verifiedby = request.user
        bill.receipt_verified_at = timezone.now()
        bill.save()
        
        return Response({'status': 'receipt verified'})

    @action(detail=True, methods=['POST'])
    def upload_receipt(self, request, pk=None):
        bill = self.get_object()
        if 'receipt_upload' not in request.FILES:
            return Response({'error': 'No receipt file provided'}, status=400)
        
        bill.receipt_upload = request.FILES['receipt_upload']
        bill.receipt_createat = timezone.now()
        # Generate receipt number using timestamp and user_id
        timestamp = int(timezone.now().timestamp())
        bill.receipt_num = f"RCP{timestamp}{bill.user_id}"
        # Set verification details
        bill.receipt_verified = True
        bill.receipt_verifiedby = request.user
        bill.receipt_verified_at = timezone.now()
        bill.save()
        
        return Response({
            'message': 'Receipt uploaded successfully',
            'receipt_url': bill.receipt_upload.url if bill.receipt_upload else None,
            'receipt_num': bill.receipt_num,
            'verified_by': request.user.email,
            'verified_at': bill.receipt_verified_at
        })

    @action(detail=True, methods=['GET'])
    def receipt_upload(self, request, pk=None):
        bill = self.get_object()
        if not bill.receipt_upload:
            return Response({'error': 'No receipt found'}, status=404)
        
        # Get file extension
        file_name = bill.receipt_upload.name.lower()
        if file_name.endswith('.pdf'):
            content_type = 'application/pdf'
        elif file_name.endswith(('.png', '.jpg', '.jpeg')):
            content_type = f'image/{file_name.split(".")[-1]}'
        else:
            content_type = 'application/octet-stream'
        
        response = HttpResponse(bill.receipt_upload.read(), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{bill.receipt_upload.name}"'
        return response

@api_view(['GET'])
@permission_classes([AllowAny])
def get_task_execution_status(request):
    try:
        # Check if Celery is running by trying to ping it
        try:
            from celery.task.control import inspect
            insp = inspect()
            if not insp.active():
                # Return tasks with "Not Started" status if Celery is not running
                tasks = TaskExecution.objects.all().order_by('task_name')
                task_statuses = [{
                    'id': task.id,
                    'name': task.task_name,
                    'brand': task.task_name.replace('_', ' ').title(),
                    'status': 'Not Started',
                    'last_updated': None,
                    'time_until_next': 0,
                    'progress': 0
                } for task in tasks]
                return Response(task_statuses)
        except Exception as e:
            logger.warning(f"Could not check Celery status: {str(e)}")
            # Assume Celery is not running if we can't check
            tasks = TaskExecution.objects.all().order_by('task_name')
            task_statuses = [{
                'id': task.id,
                'name': task.task_name,
                'brand': task.task_name.replace('_', ' ').title(),
                'status': 'Not Started',
                'last_updated': None,
                'time_until_next': 0,
                'progress': 0
            } for task in tasks]
            return Response(task_statuses)

        # If Celery is running, proceed with normal status calculation
        tasks = TaskExecution.objects.all().order_by('task_name')
        current_time = timezone.now()
        
        task_statuses = []
        for task in tasks:
            time_since_last_run = 0
            if task.last_run:
                time_since_last_run = (current_time - task.last_run).total_seconds()
            
            # Calculate time until next run
            time_until_next = max(0, task.interval - (time_since_last_run % task.interval))
            
            # Calculate progress percentage
            progress = min(100, (time_since_last_run % task.interval) / task.interval * 100)
            
            task_statuses.append({
                'id': task.id,
                'name': task.task_name,
                'brand': task.task_name.replace('_', ' ').title(),
                'status': task.status,
                'last_updated': task.last_run,
                'time_until_next': time_until_next,
                'progress': progress
            })
        
        return Response(task_statuses)
    except Exception as e:
        logger.error(f"Error getting task execution status: {str(e)}")
        return Response({'error': str(e)}, status=500)

# Alias for backward compatibility
get_task_status = get_task_execution_status

@api_view(['GET'])
@permission_classes([AllowAny])
def get_stations_status(request):
    try:
        stations = Station.objects.all().select_related('brand')
        current_time = timezone.now()
        
        station_statuses = []
        for station in stations:
            # Get latest health log
            latest_health = station.health_logs.order_by('-created_at').first()
            
            # Calculate time until next update based on brand
            interval = 3600 if station.brand.name == '3D_Paws' else 60
            time_since_last = 0
            if latest_health:
                time_since_last = (current_time - latest_health.created_at).total_seconds()
            
            time_until_next = max(0, interval - (time_since_last % interval))
            progress = min(100, (time_since_last % interval) / interval * 100)
            
            station_statuses.append({
                'id': station.id,
                'name': station.name,
                'brand': station.brand.name,
                'status': latest_health.connectivity_status if latest_health else 'Unknown',
                'last_updated': latest_health.created_at if latest_health else None,
                'time_until_next': time_until_next,
                'progress': progress
            })
        
        return Response(station_statuses)
    except Exception as e:
        logger.error(f"Error getting stations status: {str(e)}")
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def latest_station_health(request):
    # Get timestamp for 1 hour ago
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Only get weather stations (3D_Paws, Allmeteo, or Zentra)
    stations = Station.objects.filter(
        brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra'],
        health_logs__created_at__gte=one_hour_ago
    ).distinct().annotate(
        latest_battery_status=Subquery(
            StationHealthLog.objects.filter(
                station=OuterRef('pk'),
                created_at__gte=one_hour_ago
            ).order_by('-created_at').values('battery_status')[:1]
        )
    ).values('id', 'name', 'latest_battery_status')
    
    return Response(list(stations))

@api_view(['GET'])
def station_health_logs(request):
    """Get latest health logs for stations."""
    try:
        cache_key = f"station_health_logs:{request.get_full_path()}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)
        # Get parameters
        brands = request.query_params.get('brands', '3D_Paws,Allmeteo,Zentra,AWS')
        brand_list = brands.split(',')

        # Annotate each station with the latest health log id
        latest_log_subquery = StationHealthLog.objects.filter(
            station=OuterRef('pk')
        ).order_by('-created_at').values('id')[:1]

        stations = Station.objects.filter(
            brand__name__in=brand_list
        ).annotate(
            latest_log_id=Subquery(latest_log_subquery)
        ).select_related('brand')

        # Get the latest health logs in a single query
        latest_logs = StationHealthLog.objects.filter(
            id__in=[s.latest_log_id for s in stations if s.latest_log_id]
        ).select_related('station', 'station__brand')

        response_data = {
            'data': [{
                'id': log.station.id,
                'name': log.station.name,
                'battery_status': log.battery_status,
                'connectivity_status': log.connectivity_status,
                'created_at': log.created_at,
                'station': log.station_id,
                'brand': log.station.brand.name if log.station.brand else None
            } for log in latest_logs],
            'total': stations.count(),
            'page': 1,
            'page_size': 100
        }
        cache.set(cache_key, response_data, timeout=10)
        return Response(response_data)

    except Exception as e:
        import traceback
        print(f"Error in station_health_logs: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'data': [],
            'total': 0,
            'page': 1,
            'page_size': 100,
            'error': str(e)
        })

@api_view(['GET'])
def station_temperature_overview(request):
    # Get current time and 12 hours ago
    now = timezone.now()
    yesterday = now - timedelta(hours=12)
    
    # Get all stations with their latest measurements
    stations = Station.objects.filter(
        brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra']
    ).prefetch_related('measurements')
    
    response_data = []
    for station in stations:
        # Get latest temperature
        latest_temp = station.measurements.filter(
            parameter_code__in=['bt1', 'mt1'],
            date_time__gte=yesterday
        ).order_by('-date_time').first()
        
        # Get temperature history
        temp_history = station.measurements.filter(
            parameter_code__in=['bt1', 'mt1'],
            date_time__gte=yesterday
        ).order_by('date_time').values_list('value', flat=True)
        
        response_data.append({
            'id': station.id,
            'name': station.name,
            'brand_name': station.brand.name,
            'current_temperature': latest_temp.value if latest_temp else None,
            'temperature_history': list(temp_history),
            'battery_status': station.latest_health.battery_status if station.latest_health else 'Unknown',
            'last_updated': latest_temp.date_time if latest_temp else None
        })
    
    return Response(response_data)

@api_view(['GET'])
def aws_station_health_logs(request):
    """Get AWS station health logs in a format compatible with the frontend."""
    try:
        # Get AWS stations data
        stations = Station.objects.filter(
            brand__name='AWS'
        ).select_related('brand')
        
        response_data = {
            'data': [],
            'total': stations.count(),
            'page': 1,
            'page_size': 100
        }
        
        # Get timestamp for 24 hours ago
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        
        # Get the latest health logs in a single query, only from last 24 hours
        station_logs = {}
        latest_logs = StationHealthLog.objects.filter(
            station_id__in=[s.id for s in stations],
            created_at__gte=twenty_four_hours_ago
        ).order_by('-created_at')
        
        for log in latest_logs:
            if log.station_id not in station_logs:
                station_logs[log.station_id] = log
        
        # Format the data
        for station in stations:
            log = station_logs.get(station.id)
            
            # Default status is Offline if no data in last 24 hours
            status = 'Offline'
            connectivity_status = 'No Data'
            created_at = None
            
            if log:
                if log.connectivity_status and log.connectivity_status != 'Unknown' and log.connectivity_status != 'No Data':
                    connectivity_status = log.connectivity_status
                    # Only mark as online if we have recent data and connectivity is Excellent
                    if connectivity_status == 'Excellent':
                        status = 'Online'
                created_at = log.created_at
            
            # Update station's is_active field based on recent data
            station.is_active = status == 'Online'
            station.save(update_fields=['is_active'])
            
            response_data['data'].append({
                'id': station.id,
                'name': station.name,
                'connectivity_status': connectivity_status,
                'created_at': created_at,
                'station': station.id,
                'brand': 'AWS',
                'status': status
            })
        
        return Response(response_data)
    except Exception as e:
        print(f"Error in aws_station_health_logs: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'data': [],
            'total': 0,
            'page': 1,
            'page_size': 100,
            'error': str(e)
        })

@api_view(['GET'])
def get_latest_health_logs(request):
    """Get latest health logs for all stations."""
    try:
        # Get parameters
        brands = request.query_params.get('brands', '3D_Paws,Allmeteo,Zentra,AWS')
        brand_list = brands.split(',')

        # Get stations with their latest health log using subquery
        stations = Station.objects.filter(
            brand__name__in=brand_list
        ).annotate(
            latest_health=Subquery(
                StationHealthLog.objects.filter(
                    station=OuterRef('pk')
                ).order_by('-created_at').values('id')[:1]
            )
        ).select_related('brand')

        # Get the latest health logs in a single query
        latest_logs = StationHealthLog.objects.filter(
            id__in=[s.latest_health for s in stations if s.latest_health]
        ).select_related('station', 'station__brand')

        # Create a dictionary for quick lookup
        station_logs = {}
        for log in latest_logs:
            station_logs[log.station_id] = log

        # Format the response data
        response_data = []
        for station in stations:
            log = station_logs.get(station.id)
            if log:
                response_data.append({
                    'id': log.id,
                    'station_id': station.id,
                    'name': station.name,
                    'battery_status': log.battery_status,
                    'connectivity_status': log.connectivity_status,
                    'created_at': log.created_at,
                    'brand': station.brand.name if station.brand else None
                })

        return Response(response_data)

    except Exception as e:
        import traceback
        print(f"Error in get_latest_health_logs: {str(e)}")
        print(traceback.format_exc())
        return Response([], status=500)

class Command(BaseCommand):
    help = 'Update AWS station health logs with default values'

    def handle(self, *args, **options):
        # Get all AWS stations
        aws_stations = Station.objects.filter(brand__name='AWS')
        
        # Create health logs with default values
        now = timezone.now()
        for station in aws_stations:
            StationHealthLog.objects.create(
                station=station,
                battery_status='100%',
                connectivity_status='Excellent',
                created_at=now
            )
            
            # Update station's is_active field
            station.is_active = True
            station.save(update_fields=['is_active'])
            
        self.stdout.write(self.style.SUCCESS(f'Updated {aws_stations.count()} AWS stations'))

@api_view(['GET'])
def inactive_sensors(request):
    try:
        now = timezone.now()
        twenty_four_hours_ago = now - timedelta(hours=24)

        # Get query parameters
        brand = request.query_params.get('brand')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 5)) # Default to 5 as per frontend component

        # Get stations, filtered by brand if provided
        stations_queryset = Station.objects.filter(
            brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT']
        ).select_related('brand')

        if brand:
            stations_queryset = stations_queryset.filter(brand__name=brand)

        # Get all station IDs for the filtered stations
        station_ids = list(stations_queryset.values_list('id', flat=True))

        # Fetch the latest measurement for *each* sensor associated with these stations within the last 24 hours
        # This uses a Window function to get the latest measurement per sensor
        latest_measurements_subquery = Measurement.objects.filter(
            station_id__in=station_ids,
            date__gte=twenty_four_hours_ago.date() # Filter by date for potentially large tables
        ).annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=['station', 'sensor'],
                order_by=['-date', '-time']
            )
        ).filter(row_number=1)

        # Execute the subquery and create a lookup dictionary
        latest_measurements_dict = {}
        for m in latest_measurements_subquery:
            # Use a combined key for station and sensor
            latest_measurements_dict[(m.station_id, m.sensor_id)] = m

        # Collect all potential inactive sensors
        all_inactive_sensors_list = []
        # Always show all brands in the tab list
        available_brands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT']

        # Iterate through stations and their sensors to determine inactivity
        # Prefetch sensors to avoid N+1 queries in this loop
        stations_with_sensors = stations_queryset.prefetch_related('station_sensors__sensor')

        for station in stations_with_sensors:
            station_sensors = station.station_sensors.all()

            for station_sensor in station_sensors:
                sensor = station_sensor.sensor
                if not sensor: # Skip if sensor relationship is null
                    continue

                # Look up the latest measurement from the pre-fetched dictionary
                latest = latest_measurements_dict.get((station.id, sensor.id))

                # Determine status and add to the list if inactive or no data
                status = 'Active' # Assume active initially
                last_reading_dt = None

                if latest:
                     last_reading_dt = timezone.make_aware(datetime.combine(latest.date, latest.time)) if latest.date and latest.time else None
                     # Consider a sensor inactive if its last reading is older than 24 hours or value is invalid
                     if last_reading_dt < twenty_four_hours_ago:
                          status = 'Inactive'
                     elif latest.value is None or latest.value == -999:
                           status = 'No Reading' # Or another appropriate status for invalid data
                     # If latest exists and is within 24 hours and value is valid, status remains 'Active'
                else:
                    status = 'No Data' # No measurements found at all within the last 24 hours

                if status != 'Active':
                     all_inactive_sensors_list.append({
                        'station_name': station.name,
                        'brand_name': station.brand.name,
                        'sensor_type': sensor.type, # Use sensor.type here
                        'last_reading': last_reading_dt.isoformat() if last_reading_dt else None,
                        'status': status
                    })

        # Apply pagination to the collected list
        total_count = len(all_inactive_sensors_list)
        total_pages = (total_count + page_size - 1) // page_size

        start = (page - 1) * page_size
        end = start + page_size
        paginated_inactive_sensors = all_inactive_sensors_list[start:end]

        return Response({
            'results': paginated_inactive_sensors,
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'available_brands': available_brands
        })

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in inactive_sensors view: {str(e)}")
        return Response({
            'results': [],
            'total_count': 0,
            'page': 1,
            'page_size': page_size,
            'total_pages': 1,
            'error': str(e)
        }, status=500)

class ApiKeyUsageLogViewSet(viewsets.ModelViewSet):
    queryset = ApiKeyUsageLog.objects.all()
    serializer_class = ApiKeyUsageLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ApiKeyUsageLog.objects.all()
        
        # Filter by API key UUID if provided
        api_key_uuid = self.request.query_params.get('api_key') # Get the UUID
        if api_key_uuid:
            try:
                # Find the ApiAccessKey with the given UUID and filter by its ID
                api_access_key = ApiAccessKey.objects.get(uuid=api_key_uuid)
                queryset = queryset.filter(api_key=api_access_key) # Filter by the ApiAccessKey object
            except ApiAccessKey.DoesNotExist:
                # If UUID doesn't exist, return empty queryset
                queryset = ApiKeyUsageLog.objects.none()
            
        # Filter by user if provided
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user_id=user)
            
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
            
        return queryset.select_related('api_key', 'user')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def test_email(request):
    """Test email sending functionality"""
    try:
        recipient = request.data.get('email')
        if not recipient:
            return Response(
                {"error": "Email address is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subject = "Test Email from Your Application"
        message = "This is a test email to verify that the email sending functionality is working correctly."
        
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        if sent:
            return Response(
                {"message": f"Test email successfully sent to {recipient}"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Failed to send test email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        return Response(
            {"error": f"Error sending test email: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_api_keys(request):
    """Retrieve API keys for the current authenticated user"""
    try:
        api_keys = ApiAccessKey.objects.filter(user=request.user)
        serializer = ApiAccessKeySerializer(api_keys, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error retrieving API keys: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
