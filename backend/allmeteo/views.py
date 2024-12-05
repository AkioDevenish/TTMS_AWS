from rest_framework.viewsets import ModelViewSet
from .models import WeatherMeasurement
from .serializers import WeatherMeasurementSerializer

class WeatherMeasurementViewSet(ModelViewSet):
    """
    ViewSet for WeatherMeasurement model to handle CRUD operations.
    """
    queryset = WeatherMeasurement.objects.all()
    serializer_class = WeatherMeasurementSerializer
