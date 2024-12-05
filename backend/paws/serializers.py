# paws/serializers.py
from rest_framework import serializers
from .models import InstrumentMeasurement

class InstrumentMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentMeasurement
        fields = ['id', 'name',  'measurement_name', 'value', 'timestamp', 'is_test', 'created_at', 'updated_at']
