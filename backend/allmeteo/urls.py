from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherMeasurementViewSet

router = DefaultRouter()
router.register(r'measurements', WeatherMeasurementViewSet, basename='measurement')

urlpatterns = [
    path('', include(router.urls)),
]
