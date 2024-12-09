from rest_framework import viewsets
from .models import Brand, Instrument
from .serializers import BrandSerializer, InstrumentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Brand ViewSet to handle CRUD operations for Brand
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()  # All brands
    serializer_class = BrandSerializer  # Use the BrandSerializer
    
    # Optionally, you can add custom actions (e.g., to list instruments related to a specific brand)
    @action(detail=True, methods=['get'])
    def instruments(self, request, pk=None):
        """Custom action to retrieve instruments for a specific brand"""
        brand = self.get_object()
        instruments = brand.instruments.all()  # Get all instruments related to the brand
        serializer = InstrumentSerializer(instruments, many=True)
        return Response(serializer.data)

# Instrument ViewSet to handle CRUD operations for Instrument
class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()  # All instruments
    serializer_class = InstrumentSerializer  # Use the InstrumentSerializer

    # Optionally, add custom actions (e.g., to fetch the brand of a specific instrument)
    @action(detail=True, methods=['get'])
    def brand(self, request, pk=None):
        """Custom action to retrieve the brand for a specific instrument"""
        instrument = self.get_object()
        serializer = BrandSerializer(instrument.brand)
        return Response(serializer.data)
