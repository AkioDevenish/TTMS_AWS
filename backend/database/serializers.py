from rest_framework import serializers
from .models import (
    Brand, Sensor, Measurement, Station,
    StationHealthLog, StationSensor, ApiAccessKey,
    SystemLog, User, Notification, ApiAccessKeyStation,
    Message, Chat, UserPresence, Bill, ApiKeyUsageLog
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

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

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


class ApiAccessKeySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = ApiAccessKey
        fields = [
            'id', 'uuid', 'token_name', 'expires_at', 
            'note', 'last_used', 'created_at', 'updated_at', 'user', 'user_email'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    api_keys = ApiAccessKeySerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'username', 
            'role', 'organization', 'package', 'subscription_price', 
            'status', 'expires_at', 'created_at', 'updated_at', 'api_keys'
        ]
        read_only_fields = ['created_at', 'updated_at', 'api_keys']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    status = serializers.CharField(required=False, default='Active')
    username = serializers.CharField(required=False, read_only=True)
    package = serializers.CharField(required=True)
    subscription_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'username',
            'email', 
            'password',
            'first_name',
            'last_name', 
            'organization', 
            'package', 
            'expires_at',
            'role',
            'status',
            'subscription_price'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if not data.get('first_name') or not data.get('last_name'):
            raise serializers.ValidationError({
                'error': 'First name and last name are required'
            })
        
        # Validate role
        valid_roles = ['admin', 'user']
        if data.get('role') and data['role'].lower() not in valid_roles:
            raise serializers.ValidationError({
                'error': 'Invalid role. Must be either "admin" or "user"'
            })
            
        # Validate status
        valid_statuses = ['Active', 'Inactive', 'Suspended', 'Pending']
        if data.get('status') and data['status'] not in valid_statuses:
            raise serializers.ValidationError({
                'error': 'Invalid status'
            })

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', ''),
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            organization=validated_data.get('organization', ''),
            package=validated_data['package'],
            role=validated_data['role'],
            status=validated_data.get('status', 'Active'),
            expires_at=validated_data.get('expires_at'),
            subscription_price=validated_data['subscription_price']
        )
        return user


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.status == 'Suspended':
                    raise serializers.ValidationError(
                        'Your account has been suspended. Please contact support.'
                    )
                elif user.status == 'Inactive':
                    raise serializers.ValidationError(
                        'Your account has expired. Please renew your subscription.'
                    )
                data['user'] = user
                return data
            raise serializers.ValidationError('Invalid credentials.')
        raise serializers.ValidationError('Must include "email" and "password".')


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


class BillSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    verification_status = serializers.SerializerMethodField()
    
    def get_verification_status(self, obj):
        if obj.receipt_verified:
            return 'Verified'
        elif obj.receipt_upload:
            return 'Pending Verification'
        return 'Pending Upload'
    
    class Meta:
        model = Bill
        fields = ['id', 'user_id', 'user_email', 'bill_num', 'total', 'package', 
                 'created_at', 'updated_at', 'receipt_num', 'receipt_upload', 
                 'receipt_createat', 'receipt_verified', 'receipt_verifiedby',
                 'verification_status', 'receipt_verified_at']
        read_only_fields = ('bill_num', 'user_id', 'user_email', 'receipt_verified', 
                          'receipt_verifiedby', 'created_at', 'updated_at', 'receipt_verified_at')


class BillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('total', 'package', 'receipt_upload')


class ApiKeyUsageLogSerializer(serializers.ModelSerializer):
    api_key_name = serializers.CharField(source='api_key.token_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = ApiKeyUsageLog
        fields = [
            'id', 'api_key', 'api_key_name', 'user', 'user_email',
            'request_path', 'query_params', 'response_format',
            'status_code', 'user_agent', 'created_at'
        ]
        read_only_fields = ['created_at']