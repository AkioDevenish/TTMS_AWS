from django.urls import path
from . import views

urlpatterns = [
    # ... other urls ...
    path('station-health-logs/', views.station_health_logs, name='station-health-logs'),
    path('stations/temperature-overview/', views.station_temperature_overview, name='station-temperature-overview'),
] 