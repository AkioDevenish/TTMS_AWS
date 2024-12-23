from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet, StationViewSet, SensorViewSet,
    MeasurementViewSet, StationViewSet, StationHealthLogViewSet,
    StationSensorViewSet, APIAccessTokenViewSet, SystemLogViewSet,
    UserViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'stations', StationViewSet)
router.register(r'station-health-logs', StationHealthLogViewSet)
router.register(r'station-sensors', StationSensorViewSet)
router.register(r'api-tokens', APIAccessTokenViewSet)
router.register(r'system-logs', SystemLogViewSet)
router.register(r'users', UserViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]