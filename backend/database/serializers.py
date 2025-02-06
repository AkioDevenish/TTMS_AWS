from rest_framework import serializers
from .models import (
    Brand, Sensor, Measurement, Station,
    StationHealthLog, StationSensor, ApiAccessKey,
    SystemLog, User, Notification, ApiAccessKeyStation,
    Message, Chat, UserPresence
)
import urllib3
import json
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model, authenticate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

User = get_user_model()

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


class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = '__all__'


class DateTimeToDateField(serializers.DateField):
    def to_representation(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role', 'is_superuser', 
                 'is_staff', 'first_name', 'last_name']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'password',
            'first_name',
            'last_name', 
            'organization', 
            'package', 
            'expires_at'
        ]

    def validate(self, data):
        if not data.get('first_name') or not data.get('last_name'):
            raise serializers.ValidationError({
                'error': 'First name and last name are required'
            })
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
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

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            data['user'] = user
            return data
        raise serializers.ValidationError('Must include "email" and "password"')


class ApiAccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiAccessKey
        fields = ['id', 'uuid', 'token_name', 'created_at', 'last_used', 
                 'expires_at', 'note', 'stations']
        read_only_fields = ['id', 'uuid', 'created_at', 'last_used']


class ApiAccessKeyStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiAccessKeyStation
        fields = ['api_access_key', 'station']


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


class MessageSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 
                 'role', 'is_superuser', 'is_staff']


class MessageSerializer(serializers.ModelSerializer):
    sender = MessageSenderSerializer(read_only=True)
    time = serializers.TimeField(format='%I:%M %p', required=False)

    class Meta:
        model = Message
        fields = ['id', 'content', 'chat', 'sender', 'created_at', 'read_at', 'time']
        read_only_fields = ['sender', 'created_at', 'read_at', 'time']

    def create(self, validated_data):
        user = self.context['request'].user
        chat = validated_data.get('chat')
        
        current_time = timezone.now()
        message = Message.objects.create(
            content=validated_data.get('content'),
            chat=chat,
            sender=user,
            time=current_time.time(),
            created_at=current_time
        )
        return message


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'name', 'user', 'support_chat', 'created_at', 'messages', 'participants']
        read_only_fields = ['created_at', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        chat = Chat.objects.create(
            user=user,
            name=validated_data.get('name'),
            support_chat=validated_data.get('support_chat', False)
        )
        return chat


class UserPresenceSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    
    class Meta:
        model = UserPresence
        fields = ['user_id', 'is_online', 'last_seen']