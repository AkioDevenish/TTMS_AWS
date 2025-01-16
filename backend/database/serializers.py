from rest_framework import serializers
from .models import (
    Brand, Sensor, Measurement, Station,
    StationHealthLog, StationSensor, APIAccessToken,
    SystemLog, User, Notification
)
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Station
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)
    sensor_type = serializers.CharField(source='sensor.type', read_only=True)

    class Meta:
        model = Measurement
        fields = '__all__'


class StationHealthLogSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = StationHealthLog
        fields = '__all__'


class StationSensorSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)
    sensor_type = serializers.CharField(source='sensor.type', read_only=True)

    class Meta:
        model = StationSensor
        fields = '__all__'


class APIAccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIAccessToken
        fields = '__all__'
        extra_kwargs = {
            'token': {'write_only': True}  # Hide token in list views
        }


class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'name', 
            'email', 
            'organization', 
            'package', 
            'role',
            'is_staff',
            'is_superuser',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    remember_me = serializers.BooleanField(required=False, default=False)

def process_and_save_data(raw_data):
    # Check if raw_data is a string and try to parse it
    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    # Log the entire raw_data to understand its structure
    print(f"Raw data: {raw_data}")

    # Check if raw_data is a dictionary
    if isinstance(raw_data, dict):
        # If it's a dictionary, you might need to access a specific key
        # For example, if the data is under a key 'items', you would do:
        # raw_data = raw_data.get('items', [])

        # Log the keys to understand the structure
        print(f"Keys in raw_data: {list(raw_data.keys())}")

    # Process each item in raw_data
    for item in raw_data:
        print(f"Processing item: {item}")

        # Ensure item is a dictionary
        if not isinstance(item, dict):
            print(f"Unexpected item format: {item}")
            continue

        # Existing processing logic...