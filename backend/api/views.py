from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Max, Subquery, OuterRef
from django.utils import timezone
from datetime import timedelta
from database.models import Station, StationHealthLog

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
    # Get latest health log for each station
    latest_logs = StationHealthLog.objects.filter(
        station__brand__name__in=['3D_Paws', 'Allmeteo', 'Zentra']
    ).order_by('station_id', '-created_at').distinct('station_id')
    
    # Format the response
    response_data = [{
        'id': log.station.id,
        'name': log.station.name,
        'battery_status': log.battery_status,
        'connectivity_status': log.connectivity_status,
        'created_at': log.created_at
    } for log in latest_logs]
    
    return Response(response_data)

@api_view(['GET'])
def station_temperature_overview(request):
    # Get current time and 24 hours ago
    now = timezone.now()
    yesterday = now - timedelta(hours=24)
    
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