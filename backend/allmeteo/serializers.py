from rest_framework import serializers
from .models import WeatherMeasurement, WeatherReading

class WeatherReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherReading
        fields = '__all__'

class WeatherMeasurementSerializer(serializers.ModelSerializer):
    readings = WeatherReadingSerializer(many=True, read_only=True)

    class Meta:
        model = WeatherMeasurement
        fields = '__all__'
