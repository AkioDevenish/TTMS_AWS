from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Measurements
from .serializers import MeasurementsSerializer

class MeasurementsViewSet(viewsets.ModelViewSet):
    queryset = Measurements.objects.all()
    serializer_class = MeasurementsSerializer

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """
        Custom action to delete all Measurements records.
        """
        count, _ = Measurements.objects.all().delete()
        return Response({"message": f"{count} records deleted."})
