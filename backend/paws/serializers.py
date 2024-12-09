# paws/serializers.py
from rest_framework import serializers
from .models import Measurements

class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = ['id', 'name',  'measurement_name', 'value', 'timestamp', 'is_test', 'created_at', 'updated_at']
