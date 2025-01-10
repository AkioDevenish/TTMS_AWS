from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import WeatherMeasurement
from .serializers import WeatherMeasurementSerializer

class WeatherMeasurementViewSet(ModelViewSet):
  
    queryset = WeatherMeasurement.objects.all()
    serializer_class = WeatherMeasurementSerializer

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """
        Custom action to delete all InstrumentMeasurement records.
        """
        count, _ = WeatherMeasurement.objects.all().delete()
        return Response({"message": f"{count} records deleted."})
