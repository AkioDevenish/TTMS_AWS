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
import pytz
import datetime
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination  # Add pagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]  # Only admins can create/update/delete
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Optimized queryset with proper database optimizations"""
        # Start with optimized base queryset
        queryset = Station.objects.select_related('brand').prefetch_related(
            'station_sensors__sensor',
            'health_logs'
        )
        
        # Filter by brand if provided
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__name=brand)
        
        # Include decommissioned stations only if explicitly requested
        include_decommissioned = self.request.query_params.get('include_decommissioned', 'false').lower() == 'true'
        if not include_decommissioned:
            queryset = queryset.exclude(status='Decommissioned')
        
        # Order by name for consistent results
        queryset = queryset.order_by('name')
        
        return queryset

    def list(self, request, *args, **kwargs):
        """Override list to use pagination and optimize performance."""
        from django.core.cache import cache
        
        # Create cache key based on query parameters
        cache_key = f'stations_list_{request.query_params.get("brand", "all")}_{request.query_params.get("include_decommissioned", "false")}'
        
        # Try to get cached data first
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        queryset = self.get_queryset()
        
        # Use pagination for better performance
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data)
            # Cache the response for 5 minutes
            cache.set(cache_key, response_data.data, timeout=300)
            return response_data
        
        # Fallback to non-paginated response (for small datasets)
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data
        # Cache the response for 5 minutes
        cache.set(cache_key, response_data, timeout=300)
        return Response(response_data)

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

    def _clear_station_cache(self, brand_name):
        """Helper method to clear station-related cache in a compatible way"""
        from django.core.cache import cache
        try:
            # Try to use delete_pattern if available
            cache.delete_pattern('stations_list_*')
        except AttributeError:
            # Fallback for cache backends that don't support delete_pattern
            # Clear some common cache keys manually
            for i in range(1, 11):  # Clear first 10 pages
                cache.delete(f'stations_list_{i}')
                cache.delete(f'stations_list_page_{i}')
                cache.delete(f'stations_list_all_false')
                cache.delete(f'stations_list_all_true')
                cache.delete(f'stations_list_{brand_name}_false')
                cache.delete(f'stations_list_{brand_name}_true')

    @action(detail=True, methods=['post'])
    def decommission(self, request, pk=None):
        """Decommission a station instead of deleting it"""
        try:
            # Get the station directly to avoid queryset filtering issues
            instance = Station.objects.get(pk=pk)
            
            # Check if station is already decommissioned
            if instance.status == 'Decommissioned':
                return Response(
                    {"error": "Station is already decommissioned"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update station status to decommissioned
            instance.status = 'Decommissioned'
            instance.decommissioned_at = timezone.now()
            instance.save(update_fields=['status', 'decommissioned_at'])
            
            # Clear station overview cache to ensure decommissioned stations don't appear
            from django.core.cache import cache
            # Clear cache for all possible sensor types and pages for this brand
            for sensor_type in ['bt1', 'mt1', 'ws', 'wd', 'rg', 'bp1', 'sv1', 'si1', 'su1']:
                for page in range(1, 6):  # Clear first 5 pages
                    for page_size in [6, 10, 20]:  # Common page sizes
                        cache_key = f'station_overview_{instance.brand.name}_{sensor_type}_{page}_{page_size}_True'
                        cache.delete(cache_key)
                        cache_key = f'station_overview_{instance.brand.name}_{sensor_type}_{page}_{page_size}_False'
                        cache.delete(cache_key)
            
            # Clear station list cache to ensure fresh data
            self._clear_station_cache(instance.brand.name)
            
            serializer = self.get_serializer(instance)
            return Response(
                {"message": "Station decommissioned successfully", "station": serializer.data},
                status=status.HTTP_200_OK
            )
        except Station.DoesNotExist:
            return Response(
                {"error": "Station not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk=None):
        """Reactivate a decommissioned station"""
        try:
            # Get the station directly to avoid queryset filtering issues
            instance = Station.objects.get(pk=pk)
            
            # Check if station is decommissioned
            if instance.status != 'Decommissioned':
                return Response(
                    {"error": "Station is not decommissioned"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Reactivate station
            instance.status = 'Active'
            instance.decommissioned_at = None
            instance.save(update_fields=['status', 'decommissioned_at'])
            
            # Clear station overview cache to ensure reactivated stations appear
            from django.core.cache import cache
            # Clear cache for all possible sensor types and pages for this brand
            for sensor_type in ['bt1', 'mt1', 'ws', 'wd', 'rg', 'bp1', 'sv1', 'si1', 'su1']:
                for page in range(1, 6):  # Clear first 5 pages
                    for page_size in [6, 10, 20]:  # Common page sizes
                        cache_key = f'station_overview_{instance.brand.name}_{sensor_type}_{page}_{page_size}_True'
                        cache.delete(cache_key)
                        cache_key = f'station_overview_{instance.brand.name}_{sensor_type}_{page}_{page_size}_False'
                        cache.delete(cache_key)
            
            # Clear station list cache to ensure fresh data
            self._clear_station_cache(instance.brand.name)
            
            serializer = self.get_serializer(instance)
            return Response(
                {"message": "Station reactivated successfully", "station": serializer.data},
                status=status.HTTP_200_OK
            )
        except Station.DoesNotExist:
            return Response(
                {"error": "Station not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """Override update to clear cache when stations are modified."""
        # Get the instance to access brand name for cache clearing
        instance = self.get_object()
        self._clear_station_cache(instance.brand.name)
        
        return super().partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Override partial_update to clear cache when stations are modified."""
        # Get the instance to access brand name for cache clearing
        instance = self.get_object()
        self._clear_station_cache(instance.brand.name)
        
        return super().update(request, *args, **kwargs)


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

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

    def get_permissions(self):
        """Override permissions for specific actions"""
        if self.action == 'station_overview':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
            hours = int(request.query_params.get('hours', 12))  # Default to 12 hours
            
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

            # Get current time and determine appropriate time range
            now = timezone.now()
            
            # Use different time ranges for different brands
            if brand == 'OTT':
                # OTT stations may have less frequent data updates, use 7 days
                time_threshold = now - timedelta(days=7)
                print(f"Using 7-day time range for {brand} stations")
            else:
                # Use 12 hours for other brands to focus on recent data
                time_threshold = now - timedelta(hours=12)
                print(f"Using 12-hour time range for {brand} stations")
            
            yesterday = time_threshold
            
            # Base queryset with select_related and prefetch_related
            # Filter out decommissioned stations for dashboard overview
            stations = Station.objects.filter(
                brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron']
            ).exclude(status='Decommissioned').select_related('brand')

            if brand:
                stations = stations.filter(brand__name=brand)

            # Filter stations by sensor type if provided
            if sensor_type:
                # Map frontend sensor name to database sensor code
                mapped_sensor_type = self.get_sensor_mapping(sensor_type)
                print(f"Filtering stations by sensor type: {sensor_type} -> {mapped_sensor_type}")
                
                # Get stations that actually have this sensor type configured
                stations_with_sensor = Station.objects.filter(
                    id__in=stations.values_list('id', flat=True),
                    station_sensors__sensor__type=mapped_sensor_type
                ).distinct()
                
                print(f"Found {stations_with_sensor.count()} stations with sensor type {mapped_sensor_type}")
                
                # Special filtering for Allmeteo stations based on sensor type
                if brand == 'Allmeteo':
                    wind_sensors = [
                        'wind_Avg10', 'wind_Max10', 'wind_Min10', 'wind_Stdev10',
                        'wdir_Avg10', 'wdir_Gust10', 'wdir_Max10', 'wdir_Min10', 'wdir_Stdev10'
                    ]
                    if sensor_type in wind_sensors:
                        # Only show wind stations for wind sensors
                        stations_with_sensor = stations_with_sensor.filter(
                            name__icontains='Wind'
                        )
                    else:
                        # Only show helix stations for non-wind sensors
                        stations_with_sensor = stations_with_sensor.filter(
                            name__icontains='Helix'
                        )
                
                # Only apply sensor filtering if we found stations with the sensor
                # Otherwise, show all stations (they might have data from other sources)
                if stations_with_sensor.exists():
                    stations = stations_with_sensor
                    print(f"Applied sensor filtering, showing {stations.count()} stations")
                else:
                    print(f"No stations found with sensor type {mapped_sensor_type}, showing all stations")
                    # Don't filter by sensor type if no stations have it configured
                    # This allows showing stations that might have data from other sources

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
                # Get the latest measurement for this station and sensor type
                latest_measurement = None
                
                if sensor_type:
                    # Map frontend sensor name to database sensor code
                    mapped_sensor_type = self.get_sensor_mapping(sensor_type)
                    
                    # Get recent measurements based on the appropriate time range
                    measurement_query = Measurement.objects.filter(
                        station_id=station.id,
                        sensor__type=mapped_sensor_type,
                        date__gte=yesterday.date()
                    )
                    
                    print(f"Station {station.name}: Looking for measurements with sensor type {mapped_sensor_type} from {yesterday.date()}")
                    print(f"  Query found {measurement_query.count()} measurements")
                    
                    latest_measurement = measurement_query.order_by('-date', '-time').first()
                    
                    if latest_measurement:
                        print(f"  Latest measurement: {latest_measurement.date} {latest_measurement.time} - Value: {latest_measurement.value}")
                    else:
                        print(f"  No measurements found for this sensor type")
                
                station_data = {
                    'id': station.id,
                    'name': station.name,
                    'address': station.address,
                    'brand': station.brand.name,
                    'sensor_unit': self.get_sensor_unit(sensor_type),
                    'latest_measurement': {
                        'value': float(latest_measurement.value) if latest_measurement else None,
                        'date': latest_measurement.date.isoformat() if latest_measurement else None,
                        'time': self.convert_time_to_local(latest_measurement.date, latest_measurement.time) if latest_measurement else None,
                        'status': latest_measurement.status if latest_measurement else 'No Data'
                    } if latest_measurement else None,
                    # Add station health information
                    'station_health': {
                        'has_recent_data': latest_measurement is not None,
                        'has_any_recent_data': False,  # Will be populated below
                        'last_data_time': latest_measurement.date.isoformat() if latest_measurement else None
                    }
                }
                
                # Check if station has ANY recent data (not just the specific sensor type)
                if not latest_measurement:
                    any_recent_measurement = Measurement.objects.filter(
                        station_id=station.id,
                        date__gte=yesterday.date()
                    ).order_by('-date', '-time').first()
                    
                    if any_recent_measurement:
                        print(f"  Station {station.name}: No {sensor_type} data, but has recent {any_recent_measurement.sensor.type} data")
                        station_data['station_health']['has_any_recent_data'] = True
                        station_data['station_health']['last_data_time'] = any_recent_measurement.date.isoformat()
                    else:
                        print(f"  Station {station.name}: No recent data of any type")
                        station_data['station_health']['has_any_recent_data'] = False
                else:
                    # Station has data for the requested sensor type
                    station_data['station_health']['has_any_recent_data'] = True
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

    def convert_time_to_local(self, date, time):
        """Helper function to format time (data is already in local timezone)"""
        try:
            # The data is already stored in Trinidad timezone (UTC-4)
            # Just format the time as is
            if time:
                return time.strftime('%H:%M:%S')
            return None
        except Exception as e:
            print(f"Error formatting time: {e}")
            return time.isoformat() if time else None

    def get_sensor_mapping(self, sensor_type):
        """Map frontend sensor names to database sensor codes"""
        if not sensor_type:
            return None
        
        # 3D Paws sensor mapping (frontend name -> database code)
        sensor_mapping = {
            'Temperature 1': 'bt1',
            'Temperature 2': 'mt1',
            'Pressure': 'bp1',
            'Wind Speed': 'ws',
            'Wind Direction': 'wd',
            'Precipitation': 'rg',
            'Downwelling Visible': 'sv1',
            'Downwelling Infrared': 'si1',
            'Downwelling Ultraviolet': 'su1',
            'Battery Percent': 'bpc',
            'Cell Signal Strength': 'css',
            'Wind Gust': 'wg',
            'Wind Gust Direction': 'wgd',
            'Battery Cell Signal': 'bcs',
            'Heat Index': 'hth',
            'Battery Health': 'bh1',
            'Cloud Fraction': 'cfr',
            'Heat Temperature': 'ht1',
            'Heat Humidity': 'hh1',
            'Wet Bulb Globe Temperature': 'wbgt',
            'Solar Heat': 'sh1',
            'Wet Bulb Temperature': 'wbt',
            'Soil Temperature': 'st1'
        }
        
        # Zentra sensor mapping (frontend name -> database code)
        zentra_mapping = {
            'Solar Radiation': 'Solar Radiation',
            'Precipitation': 'Precipitation',
            'Lightning Activity': 'Lightning Activity',
            'Lightning Distance': 'Lightning Distance',
            'Wind Direction': 'Wind Direction',
            'Wind Speed': 'Wind Speed',
            'Gust Speed': 'Gust Speed',
            'Air Temperature': 'Air Temperature',
            'Relative Humidity': 'Relative Humidity',
            'Atmospheric Pressure': 'Atmospheric Pressure',
            'X-axis Level': 'X-axis Level',
            'Y-axis Level': 'Y-axis Level',
            'Max Precipitation Rate': 'Max Precipitation Rate',
            'RH Sensor Temperature': 'RH Sensor Temperature',
            'Vapor Pressure Deficit': 'Vapor Pressure Deficit',
            'Battery Percent': 'Battery Percent',
            'Battery Voltage': 'Battery Voltage',
            'Atmospheric Pressure (Reference Pressure)': 'Atmospheric Pressure (Reference Pressure)'
        }
        
        # OTT sensor mapping (frontend name -> database code)
        ott_mapping = {
            '5 min rain': '5 min rain',
            'Air Temperature': 'Air Temperature',
            'Barometric Pressure': 'Barometric Pressure',
            'Baro Tendency': 'Baro Tendency',
            'Battery': 'Battery',
            'Daily Rain': 'Daily Rain',
            'Dew Point': 'Dew Point',
            'Gust Direction': 'Gust Direction',
            'Gust Speed': 'Gust Speed',
            'Hours of Sunshine': 'Hours of Sunshine',
            'Maximum Air Temperature': 'Maximum Air Temperature',
            'Minimum Air Temperature': 'Minimum Air Temperature',
            'Relative Humidity': 'Relative Humidity',
            'Solar Radiation Avg': 'Solar Radiation Avg',
            'Solar Radiation Total': 'Solar Radiation Total',
            'Wind Dir Average': 'Wind Dir Average',
            'Wind Dir Inst': 'Wind Dir Inst',
            'Wind Speed Average': 'Wind Speed Average',
            'Wind Speed Inst': 'Wind Speed Inst'
        }
        
        # Sutron sensor mapping (frontend name -> database code)
        sutron_mapping = {
            'AT': 'AT',
            'ATMAX': 'ATMAX',
            'ATMIN': 'ATMIN',
            'AT_ADJUSTED': 'AT_ADJUSTED',
            'BARO': 'BARO',
            'BATT': 'BATT',
            'DP': 'DP',
            'GUST': 'GUST',
            'GUSTDIR': 'GUSTDIR',
            'HRSSUN': 'HRSSUN',
            'LEAF DRY': 'LEAF DRY',
            'LEAF SLIGHT WET': 'LEAF SLIGHT WET',
            'LEAF WET': 'LEAF WET',
            'LEAFW': 'LEAFW',
            'LWC': 'LWC',
            'LWTIME': 'LWTIME',
            'QFE': 'QFE',
            'QFF': 'QFF',
            'QNH': 'QNH',
            'RAIN': 'RAIN',
            'RAINDAILY': 'RAINDAILY',
            'RH': 'RH',
            'SOILCOND': 'SOILCOND',
            'SOILEC': 'SOILEC',
            'SOILM': 'SOILM',
            'SOILPERM': 'SOILPERM',
            'SOILT': 'SOILT',
            'SOLARV': 'SOLARV',
            'SOLARVOLTAGE': 'SOLARVOLTAGE',
            'SOLRAD': 'SOLRAD',
            'UNKNOWN': 'UNKNOWN',
            'WD10': 'WD10',
            'WDA': 'WDA',
            'WDI': 'WDI',
            'WS10': 'WS10',
            'WSA': 'WSA',
            'WSI': 'WSI',
            'BATTERY': 'BATTERY'
        }
        
        # Check if it's a Zentra sensor type first
        if sensor_type in zentra_mapping:
            return zentra_mapping[sensor_type]
        
        # Check if it's an OTT sensor type
        if sensor_type in ott_mapping:
            return ott_mapping[sensor_type]
        
        # Check if it's a Sutron sensor type
        if sensor_type in sutron_mapping:
            return sutron_mapping[sensor_type]
        
        # If the sensor_type is already a database code (like 'bt1'), return it as-is
        # If it's a frontend name (like 'Temperature 1'), map it to database code
        return sensor_mapping.get(sensor_type, sensor_type)
    
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
            'wg': 'm/s',
            'wgd': '°',
            'bcs': '%',
            'hth': '°C',
            'bh1': '%',
            'cfr': '%',
            'ht1': '°C',
            'hh1': '%',
            'wbgt': '°C',
            'hi': '°C',
            'sh1': 'W/m²',
            'wbt': '°C',
            'st1': '°C',
            'Air Temperature': '°C',
            'Wind Speed': 'm/s',
            'Precipitation': 'mm',
            'Solar Radiation': 'W/m²',
            'Relative Humidity': '%',
            'Atmospheric Pressure': 'kPa',
            'Lightning Activity': 'count',
            'Lightning Distance': 'km',
            'Gust Speed': 'm/s',
            'X-axis Level': 'mm',
            'Y-axis Level': 'mm',
            'Max Precipitation Rate': 'mm/h',
            'RH Sensor Temperature': '°C',
            'Vapor Pressure Deficit': 'kPa',
            'Battery Percent': '%',
            'Battery Voltage': 'mV',
            'Atmospheric Pressure (Reference Pressure)': 'kPa',
            # Sutron sensor units
            'AT': '°C',
            'ATMAX': '°C',
            'ATMIN': '°C',
            'AT_ADJUSTED': '°C',
            'BARO': 'hPa',
            'BATT': 'V',
            'DP': '°C',
            'GUST': 'm/s',
            'GUSTDIR': '°',
            'HRSSUN': 'hr',
            'LEAF DRY': 'status',
            'LEAF SLIGHT WET': 'status',
            'LEAF WET': 'status',
            'LEAFW': 'status',
            'LWC': 'count',
            'LWTIME': 'min',
            'QFE': 'hPa',
            'QFF': 'hPa',
            'QNH': 'hPa',
            'RAIN': 'mm',
            'RAINDAILY': 'mm',
            'RH': '%',
            'SOILCOND': 'mS/cm',
            'SOILEC': 'mS/cm',
            'SOILM': '%',
            'SOILPERM': 'dimensionless',
            'SOILT': '°C',
            'SOLARV': 'V',
            'SOLARVOLTAGE': 'V',
            'SOLRAD': 'W/m²',
            'UNKNOWN': 'unknown',
            'WD10': '°',
            'WDA': '°',
            'WDI': '°',
            'WS10': 'm/s',
            'WSA': 'm/s',
            'WSI': 'm/s',
            'BATTERY': 'V',
            'wind_ave10': 'm/s',
            'wind_Max10': 'm/s',
            'wind_Min10': 'm/s',
            'wdir_Max10': '°',
            'dir_ave10': '°',
            'battery': 'V',
            'humidity': '%',
            'irradiation': 'W/m²',
            'irradiation_max': 'W/m²',
            'pressure': 'hPa',
            'pressure_raw': 'hPa',
            'rain': 'mm',
            'rainfall_rate_max': 'mm/h',
            'temperature': '°C',
            'temperature_max': '°C',
            'temperature_min': '°C',
            'temperature_wetbulb_stull2011_C': '°C',
            'wdir_Avg10': '°',
            'wdir_Gust10': '°',
            'wdir_Min10': '°',
            'wdir_Stdev10': '°',
            'wind_Avg10': 'm/s',
            'wind_Stdev10': 'm/s',
            'dewPoint': '°C',
            # OTT sensor types
            '5 min rain': 'mm',
            'Air Temperature': '°C',
            'Barometric Pressure': 'hPa',
            'Baro Tendency': 'hPa',
            'Battery': 'V',
            'Daily Rain': 'mm',
            'Dew Point': '°C',
            'Gust Direction': '°',
            'Gust Speed': 'knots',
            'Hours of Sunshine': 'hr',
            'Maximum Air Temperature': '°C',
            'Minimum Air Temperature': '°C',
            'Relative Humidity': '%',
            'Solar Radiation Avg': 'Wh/m²',
            'Solar Radiation Total': 'Wh/m²',
            'Wind Dir Average': '°',
            'Wind Dir Inst': '°',
            'Wind Speed Average': 'knots',
            'Wind Speed Inst': 'knots'
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
            print("History endpoint called with params:", request.GET)
            station_ids_param = request.GET.get('station_ids', '')
            sensor_type_param = request.GET.get('sensor_type')
            hours = int(request.GET.get('hours', 12))  # Default to 12 hours
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
            
            # Get the brand name to determine time range
            station_ids_list = [int(id) for id in station_ids_param.split(',')]
            stations = Station.objects.filter(id__in=station_ids_list).select_related('brand')
            
            # Check if any of the requested stations are 3D Paws
            paws_stations = stations.filter(brand__name='3D_Paws')
            has_paws = paws_stations.exists()
            
            # Use the requested hours for all brands (focus on recent data)
            effective_hours = hours
            print(f"Using time range of {effective_hours} hours for all brands")
            
            now = timezone.now()
            time_threshold = now - timezone.timedelta(hours=effective_hours)
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
                    'time': self.convert_time_to_local(m.date, m.time)
                })

            # Return the measurements data
            result = {
                'measurements': result_data
            }
            
            # Insert into api_key_usage logs and update Api_Access_Keys
            if hasattr(request, 'auth') and request.auth and isinstance(request.auth, ApiAccessKey):
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
                        'query_params': dict(request.GET),
                        'response_format': getattr(request, 'accepted_renderer', None),
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
            # Use iexact for case-insensitive brand matching
            queryset = queryset.filter(station__brand__name__iexact=brand)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ApiAccessKeyViewSet(viewsets.ModelViewSet):
    queryset = ApiAccessKey.objects.all()
    serializer_class = ApiAccessKeySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff or self.request.user.is_superuser:
            # Admins can see all API keys
            return ApiAccessKey.objects.all()
        else:
            # Regular users can only see their own API keys
            return ApiAccessKey.objects.filter(user=self.request.user)


class SystemLogViewSet(viewsets.ModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

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
        # Get active stations (exclude decommissioned for dashboard purposes)
        stations = Station.objects.exclude(status='Decommissioned').select_related('brand')
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
@permission_classes([AllowAny])
def get_stations_comprehensive_status(request):
    """
    Get comprehensive station status including the three-tier system:
    - Online: Stations reporting valid data within expected parameters
    - Offline: Stations not reporting data (no recent transmissions)
    - Online Erroneous Data: Stations transmitting but data fails validation
    """
    try:
        from django.db.models import Count, Q
        from datetime import timedelta
        
        # Get active stations (exclude decommissioned for dashboard purposes)
        stations = Station.objects.exclude(status='Decommissioned').select_related('brand')
        current_time = timezone.now()
        
        # Define time thresholds for different statuses
        online_threshold = timedelta(hours=1)  # 1 hour for online status
        offline_threshold = timedelta(hours=24)  # 24 hours for offline status
        
        station_statuses = []
        
        for station in stations:
            # Get latest health log
            latest_health = station.health_logs.order_by('-created_at').first()
            
            # Get latest measurements (get all first, then slice for display)
            all_measurements = station.measurements.order_by('-created_at')
            latest_measurements = all_measurements[:100]  # Last 100 measurements for display
            
            # Determine transmission status
            has_recent_transmission = False
            if all_measurements.exists():
                latest_measurement = all_measurements.first()
                time_since_last = current_time - latest_measurement.created_at
                has_recent_transmission = time_since_last <= online_threshold
            
            # Determine data quality status
            data_quality_status = 'unknown'
            invalid_data_count = 0
            total_data_count = 0
            
            if all_measurements.exists():
                # Count measurements with validation flags (use the full queryset, not the sliced one)
                invalid_data_count = all_measurements.filter(flag=False).count()
                total_data_count = all_measurements.count()
                
                if total_data_count > 0:
                    invalid_percentage = (invalid_data_count / total_data_count) * 100
                    if invalid_percentage > 50:  # More than 50% invalid data
                        data_quality_status = 'erroneous'
                    elif invalid_percentage > 10:  # More than 10% invalid data
                        data_quality_status = 'warning'
                    else:
                        data_quality_status = 'good'
            
            # Determine overall status based on three-tier system
            if not has_recent_transmission:
                overall_status = 'Offline'
                status_code = 'offline'
                status_description = 'Station not reporting data (no recent transmissions)'
                status_color = '#dc3545'  # Red
            elif data_quality_status == 'erroneous':
                overall_status = 'Online Erroneous Data'
                status_code = 'online_erroneous'
                status_description = 'Station transmitting but data fails validation'
                status_color = '#ffc107'  # Yellow/Orange
            else:
                overall_status = 'Online'
                status_code = 'online'
                status_description = 'Station reporting valid data within expected parameters'
                status_color = '#28a745'  # Green
            
            # Calculate additional metrics
            time_since_last = 0
            if latest_measurements.exists():
                time_since_last = (current_time - latest_measurements.first().created_at).total_seconds()
            
            # Get brand-specific update interval
            interval = 3600 if station.brand.name == '3D_Paws' else 60
            time_until_next = max(0, interval - (time_since_last % interval))
            progress = min(100, (time_since_last % interval) / interval * 100)
            
            station_statuses.append({
                'id': station.id,
                'name': station.name,
                'brand': station.brand.name,
                'serial_number': station.serial_number,
                'overall_status': overall_status,
                'status_code': status_code,
                'status_description': status_description,
                'status_color': status_color,
                'transmission_status': 'Active' if has_recent_transmission else 'Inactive',
                'data_quality_status': data_quality_status,
                'data_quality_metrics': {
                    'total_measurements': total_data_count,
                    'invalid_measurements': invalid_data_count,
                    'valid_measurements': total_data_count - invalid_data_count,
                    'invalid_percentage': round((invalid_data_count / total_data_count) * 100, 2) if total_data_count > 0 else 0
                },
                'last_updated': latest_measurements.first().created_at if latest_measurements.exists() else None,
                'time_since_last_update': time_since_last,
                'time_until_next_update': time_until_next,
                'progress': progress,
                'health_info': {
                    'battery_status': latest_health.battery_status if latest_health else 'Unknown',
                    'connectivity_status': latest_health.connectivity_status if latest_health else 'Unknown',
                    'last_health_check': latest_health.created_at if latest_health else None
                }
            })
        
        return Response({
            'stations': station_statuses,
            'summary': {
                'total_stations': len(station_statuses),
                'online': len([s for s in station_statuses if s['status_code'] == 'online']),
                'offline': len([s for s in station_statuses if s['status_code'] == 'offline']),
                'online_erroneous': len([s for s in station_statuses if s['status_code'] == 'online_erroneous'])
            },
            'timestamp': current_time
        })
        
    except Exception as e:
        logger.error(f"Error getting comprehensive stations status: {str(e)}")
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def latest_station_health(request):
    # Get timestamp for 1 hour ago
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Only get weather stations (3D_Paws, Allmeteo, Zentra, OTT, or Sutron)
    stations = Station.objects.filter(
        brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron'],
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
        brands = request.query_params.get('brands', '3D_Paws,Allmeteo,Zentra,OTT,Sutron,AWS')
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
        brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron']
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
@permission_classes([AllowAny])
def aws_station_health_logs(request):
    """Get station health logs for all brands (OTT, 3D_Paws, Allmeteo) in a format compatible with the frontend."""
    try:
        # Get query parameters
        brand = request.query_params.get('brand')  # Optional brand filter
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10
        
        # Get stations, filtered by brand if provided
        stations_queryset = Station.objects.filter(
            brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron']
        ).exclude(status='Decommissioned').select_related('brand')
        
        if brand:
            stations_queryset = stations_queryset.filter(brand__name=brand)
        
        # Get total count for pagination
        total_stations = stations_queryset.count()
        
        # Get timestamp for 24 hours ago
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        
        # Get the latest health logs for ALL stations (not paginated yet)
        station_logs = {}
        latest_logs = StationHealthLog.objects.filter(
            station_id__in=[s.id for s in stations_queryset],
            created_at__gte=twenty_four_hours_ago
        ).order_by('-created_at')
        
        for log in latest_logs:
            if log.station_id not in station_logs:
                station_logs[log.station_id] = log
        
        # Format the data for ALL stations first
        station_data = []
        for station in stations_queryset:
            log = station_logs.get(station.id)
            
            # Default status is Offline if no data in last 24 hours
            status = 'Offline'
            connectivity_status = 'No Data'
            battery_status = 'Unknown'
            created_at = None
            
            if log:
                battery_status = log.battery_status
                if log.connectivity_status and log.connectivity_status != 'Unknown' and log.connectivity_status != 'No Data':
                    connectivity_status = log.connectivity_status
                    # Mark as online if we have recent data and connectivity is good
                    if connectivity_status in ['Excellent', 'Good', 'Fair', 'Connected']:
                        status = 'Online'
                    elif connectivity_status in ['Poor', 'No Signal']:
                        status = 'Offline'
                    else:
                        status = 'Warning'
                else:
                    # For stations without connectivity status (like Allmeteo, Zentra),
                    # determine status based on battery data and data freshness
                    if battery_status != 'Unknown' and battery_status != 'No Data':
                        # If we have battery data, consider the station online
                        # Check if the data is recent (within last 24 hours)
                        if log.created_at and (timezone.now() - log.created_at).total_seconds() < 86400:  # 24 hours
                            status = 'Online'
                        else:
                            status = 'Warning'  # Data is old
                    else:
                        # Check if we have any recent data at all (even if battery is unknown)
                        if log.created_at and (timezone.now() - log.created_at).total_seconds() < 86400:  # 24 hours
                            status = 'Online'  # Has recent data, consider online
                        else:
                            status = 'Offline'  # No recent data
                    
                    # SPECIAL CASE: If battery status is excellent/good, always mark as online
                    if battery_status in ['Excellent', 'Good', 'Fair']:
                        status = 'Online'
                created_at = log.created_at
            
            station_data.append({
                'id': station.id,
                'name': station.name,
                'battery_status': battery_status,
                'connectivity_status': connectivity_status,
                'created_at': created_at,
                'station': station.id,
                'brand': station.brand.name,
                'status': status
            })
        
        # Sort stations by status priority: Offline first, then Warning, then Online
        # This makes it easier to identify problematic stations
        status_priority = {
            'Offline': 1,      # Highest priority (shown first)
            'Warning': 2,      # Medium priority
            'Online': 3        # Lowest priority (shown last)
        }
        
        station_data.sort(key=lambda x: (
            status_priority.get(x['status'], 4),  # Sort by status priority
            x['name']  # Then alphabetically by name for same status
        ))
        
        # NOW apply pagination to the sorted results
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_station_data = station_data[start_index:end_index]
        
        # Calculate pagination metadata
        total_pages = (total_stations + page_size - 1) // page_size
        has_next = page < total_pages
        has_previous = page > 1
        
        response_data = {
            'data': paginated_station_data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total_stations,
                'total_pages': total_pages,
                'has_next': has_next,
                'has_previous': has_previous,
                'next_page': page + 1 if has_next else None,
                'previous_page': page - 1 if has_previous else None
            }
        }
        
        return Response(response_data)
    except Exception as e:
        print(f"Error in aws_station_health_logs: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return Response({
            'data': [],
            'pagination': {
                'page': 1,
                'page_size': 10,
                'total': 0,
                'total_pages': 0,
                'has_next': False,
                'has_previous': False,
                'next_page': None,
                'previous_page': None
            },
            'error': str(e)
        }, status=500)

@api_view(['GET'])
def get_latest_health_logs(request):
    """Get latest health logs for all stations."""
    try:
        # Get parameters
        brands = request.query_params.get('brands', '3D_Paws,Allmeteo,Zentra,OTT,Sutron,AWS')
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
        current_hour_start = now.replace(minute=0, second=0, microsecond=0)
        one_hour_ago = current_hour_start - timedelta(hours=1)

        # Get query parameters
        brand = request.query_params.get('brand')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20)) # Default to 20 as per frontend component

        # Get stations, filtered by brand if provided
        # Exclude decommissioned stations for dashboard purposes
        stations_queryset = Station.objects.filter(
            brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron']
        ).exclude(status='Decommissioned').select_related('brand')

        if brand:
            stations_queryset = stations_queryset.filter(brand__name=brand)

        # Get all station IDs for the filtered stations
        station_ids = list(stations_queryset.values_list('id', flat=True))

        # Fetch the latest measurement for *each* sensor associated with these stations within the last 7 days
        # This uses a Window function to get the latest measurement per sensor
        seven_days_ago = now - timedelta(days=7)
        latest_measurements_subquery = Measurement.objects.filter(
            station_id__in=station_ids,
            date__gte=seven_days_ago.date() # Filter by date for potentially large tables
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
        available_brands = ['3D_Paws', 'Allmeteo', 'Zentra', 'OTT', 'Sutron']

        # Get sensors that have had measurements in the last 7 days (to be more lenient about recent activity)
        # This accounts for potential timezone issues and data fetcher delays
        recent_sensors = Measurement.objects.filter(
            station_id__in=station_ids,
            date__gte=seven_days_ago.date()
        ).values_list('station_id', 'sensor_id').distinct()
        
        # Create a set for faster lookup
        recent_sensors_set = set(recent_sensors)
        
        # Get all sensors that have EVER had measurements for these stations (to avoid checking unconfigured sensors)
        all_configured_sensors = Measurement.objects.filter(
            station_id__in=station_ids
        ).values_list('station_id', 'sensor_id').distinct()
        
        # Create a set for faster lookup
        configured_sensors_set = set(all_configured_sensors)

        # Iterate through stations and their sensors to determine inactivity
        # Prefetch sensors to avoid N+1 queries in this loop
        stations_with_sensors = stations_queryset.prefetch_related('station_sensors__sensor')

        for station in stations_with_sensors:
            station_sensors = station.station_sensors.all()

            for station_sensor in station_sensors:
                sensor = station_sensor.sensor
                if not sensor: # Skip if sensor relationship is null
                    continue

                # Check if this sensor has had any measurements in the last 3 days
                has_recent_data = (station.id, sensor.id) in recent_sensors_set
                
                # Check if this sensor has had any historical data
                has_any_data = (station.id, sensor.id) in configured_sensors_set
                
                if not has_any_data:
                    # Sensor has never had any data - add it to the inactive list with "No Reading"
                    all_inactive_sensors_list.append({
                        'station_name': station.name,
                        'brand_name': station.brand.name,
                        'sensor_type': sensor.type,
                        'last_reading': None,
                        'status': 'No Reading'
                    })
                    continue
                
                # If no recent data but has historical data, check if the historical data is problematic
                if not has_recent_data:
                    # Get the latest measurement to check if it has problematic values
                    latest = latest_measurements_dict.get((station.id, sensor.id))
                    if latest:
                        last_reading_dt = timezone.make_aware(datetime.combine(latest.date, latest.time)) if latest.date and latest.time else None
                        
                        # Check for problematic data values
                        if latest.value is None or latest.value == -999:
                            status = 'No Reading'
                        elif last_reading_dt and last_reading_dt < one_hour_ago:
                            # Sensor has old data and hasn't reported recently - mark as inactive
                            status = 'No Reading'
                        else:
                            # Sensor has valid recent data - skip it
                            continue
                        
                        # Add problematic sensors to the list
                        all_inactive_sensors_list.append({
                            'station_name': station.name,
                            'brand_name': station.brand.name,
                            'sensor_type': sensor.type,
                            'last_reading': last_reading_dt.isoformat() if last_reading_dt else None,
                            'status': status
                        })
                    continue

                # Look up the latest measurement from the pre-fetched dictionary
                latest = latest_measurements_dict.get((station.id, sensor.id))

                # Determine status and add to the list if inactive or no data
                status = 'Active' # Assume active initially
                last_reading_dt = None

                if latest:
                     last_reading_dt = timezone.make_aware(datetime.combine(latest.date, latest.time)) if latest.date and latest.time else None
                     # Only consider sensors with invalid data values, not old data
                     if latest.value is None or latest.value == -999:
                           status = 'No Reading' # Invalid data

                     else:
                           # Sensor has valid recent data - skip it
                           continue
                else:
                    # This shouldn't happen since we already checked has_any_data above
                    # But just in case, skip this sensor
                    continue

                # Only add sensors that have no reading
                if status == 'No Reading':
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
        
        # Debug: Check paginated results
        print(f"DEBUG: Paginated results (page {page}):")
        for i, sensor in enumerate(paginated_inactive_sensors[:5]):
            print(f"  {i+1}. {sensor['station_name']} -> {sensor['sensor_type']} -> Status: '{sensor['status']}' -> Last: {sensor['last_reading']}")

        # Add debugging information
        print(f"DEBUG: Total inactive sensors found: {total_count}")
        print(f"DEBUG: Sensors with recent measurements (7 days): {len(recent_sensors_set)}")
        print(f"DEBUG: Total configured sensors (ever): {len(configured_sensors_set)}")
        print(f"DEBUG: Total stations: {stations_queryset.count()}")
        print(f"DEBUG: Brand filter: {brand}")
        print(f"DEBUG: Performance improvement: Skipped {len(stations_with_sensors) * len(stations_with_sensors[0].station_sensors.all()) - len(configured_sensors_set)} unconfigured sensor combinations")
        
        # Additional debugging for OTT stations
        if brand == 'OTT' or not brand:
            ott_stations = [s for s in stations_with_sensors if s.brand.name == 'OTT']
            for station in ott_stations:
                station_sensors = station.station_sensors.all()
                print(f"DEBUG: OTT Station {station.name} has {len(station_sensors)} sensor relationships")
                for ss in station_sensors[:3]:  # Show first 3 sensors
                    sensor = ss.sensor
                    if sensor:
                        latest_measurement = Measurement.objects.filter(
                            station=station,
                            sensor=sensor
                        ).order_by('-date', '-time').first()
                        if latest_measurement:
                            print(f"DEBUG:   Sensor {sensor.type}: Latest measurement {latest_measurement.date} {latest_measurement.time}")
                        else:
                            print(f"DEBUG:   Sensor {sensor.type}: No measurements found")
        
        # Debug: Show sample of inactive sensors (current hour)
        if all_inactive_sensors_list:
            print(f"DEBUG: Sample inactive sensors (current hour):")
            for i, sensor in enumerate(all_inactive_sensors_list[:10]):
                print(f"  {i+1}. {sensor['station_name']} -> {sensor['brand_name']} -> {sensor['sensor_type']} -> Status: '{sensor['status']}' -> Last Reading: {sensor['last_reading']}")
        else:
            print(f"DEBUG: No inactive sensors found in current hour")
            
        # Debug: Check for T10 Paramin specifically
        t10_sensors = [s for s in all_inactive_sensors_list if 'T10' in s['station_name']]
        if t10_sensors:
            print(f"DEBUG: T10 Paramin sensors found: {len(t10_sensors)}")
            for sensor in t10_sensors:
                print(f"  - {sensor['station_name']} -> {sensor['sensor_type']} -> {sensor['status']}")
        else:
            print(f"DEBUG: No T10 Paramin sensors found in inactive list")

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
