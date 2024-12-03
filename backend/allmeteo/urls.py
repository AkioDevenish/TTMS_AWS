from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherMeasurementViewSet, WeatherReadingViewSet

router = DefaultRouter()
router.register(r'measurements', WeatherMeasurementViewSet, basename='measurement')
router.register(r'readings', WeatherReadingViewSet, basename='reading')

urlpatterns = [
    path('', include(router.urls)),
]
