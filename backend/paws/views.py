# paws/views.py
from rest_framework import viewsets
from .models import InstrumentMeasurement
from .serializers import InstrumentMeasurementSerializer

class InstrumentMeasurementViewSet(viewsets.ModelViewSet):
    queryset = InstrumentMeasurement.objects.all()
    serializer_class = InstrumentMeasurementSerializer
