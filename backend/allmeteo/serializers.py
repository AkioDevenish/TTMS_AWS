from rest_framework import serializers
from .models import WeatherMeasurement

class WeatherMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherMeasurement
        fields = '__all__'
