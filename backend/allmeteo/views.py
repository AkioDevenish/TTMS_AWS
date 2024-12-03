from rest_framework.viewsets import ModelViewSet
from .models import WeatherMeasurement, WeatherReading
from .serializers import WeatherMeasurementSerializer, WeatherReadingSerializer

class WeatherMeasurementViewSet(ModelViewSet):
    queryset = WeatherMeasurement.objects.all()
    serializer_class = WeatherMeasurementSerializer

class WeatherReadingViewSet(ModelViewSet):
    queryset = WeatherReading.objects.all()
    serializer_class = WeatherReadingSerializer
