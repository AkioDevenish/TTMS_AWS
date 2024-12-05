from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InstrumentMeasurement
from .serializers import InstrumentMeasurementSerializer

class InstrumentMeasurementViewSet(viewsets.ModelViewSet):
    queryset = InstrumentMeasurement.objects.all()
    serializer_class = InstrumentMeasurementSerializer

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """
        Custom action to delete all InstrumentMeasurement records.
        """
        count, _ = InstrumentMeasurement.objects.all().delete()
        return Response({"message": f"{count} records deleted."})
