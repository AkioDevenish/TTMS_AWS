from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
import json
from django.core.exceptions import ValidationError
import uuid
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Management
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

def generate_username():
    return f"user_{uuid.uuid4().hex[:8]}"

class User(AbstractUser):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Pending', 'Pending'),
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        default=generate_username
    )
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    PACKAGE_PRICES = {
        'Weekly': 1500,
        'Monthly': 3000,
        'Yearly': 6000
    }

    package = models.CharField(max_length=10, choices=[
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly')
    ], default='Monthly')
    
    subscription_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    role = models.CharField(max_length=50, default='user')
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    class Meta:
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def clean(self):
        super().clean()
        if not self.first_name or not self.last_name:
            raise ValidationError('First name and last name are required')

    def save(self, *args, **kwargs):
        if not self.username or (self.first_name and self.last_name):
            base_username = f"{self.first_name.lower()}.{self.last_name.lower()}"
            username = base_username
            counter = 1
            # Check if username exists and generate a unique one
            while User.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_initial_bill(sender, instance, created, **kwargs):
    if created:
        Bill.objects.create(
            user=instance,
            total=instance.subscription_price,  
            package=instance.package,
            bill_num=f"{int(timezone.now().timestamp())}{instance.id}"
        )

# Core Models
class Brand(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name

class Station(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="stations")
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    last_updated_at = models.DateTimeField()
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    installation_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    sensors = models.ManyToManyField('Sensor', through='StationSensor', related_name='stations')

    class Meta:
        db_table = 'stations'

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

class Sensor(models.Model):
    type = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    class Meta:
        db_table = 'sensors'

    def __str__(self):
        return f"{self.type} ({self.unit})"

# Measurement and Monitoring
class Measurement(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='measurements')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements', null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField()
    status = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'measurements'

    def __str__(self):
        return f"{self.station} - {self.sensor} - {self.date} {self.time}"

class StationHealthLog(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='health_logs')
    battery_status = models.CharField(max_length=50)
    connectivity_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'station_health_logs'

    def __str__(self):
        return f"{self.station} - {self.created_at}"

# Relationships and Access Control
class StationSensor(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='station_sensors')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='station_sensors')

    class Meta:
        db_table = 'station_sensors'
        unique_together = ('station', 'sensor')

    def __str__(self):
        return f"{self.station} - {self.sensor}"

class ApiAccessKey(models.Model):
    uuid = models.UUIDField(unique=True)
    token_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    stations = models.ManyToManyField(Station, through='ApiAccessKeyStation')
    expires_at = models.DateTimeField()
    note = models.TextField(null=True, blank=True)
    last_used = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_access_keys'

    def __str__(self):
        return f"{self.token_name} ({self.uuid})"

class ApiAccessKeyStation(models.Model):
    api_access_key = models.ForeignKey(ApiAccessKey, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    class Meta:
        db_table = 'api_access_key_stations'
        unique_together = ('api_access_key', 'station')

# System and Communication
class SystemLog(models.Model):
    module = models.CharField(max_length=100)
    activity = models.TextField()
    type = models.CharField(max_length=50)
    user_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_logs'

    def __str__(self):
        return f"{self.module} - {self.type} - {self.created_at}"

class Notification(models.Model):
    uuid = models.UUIDField(primary_key=True)
    type = models.CharField(max_length=50)
    notifiable_id = models.IntegerField()
    notifiable_type = models.CharField(max_length=100)
    data = models.JSONField()
    read_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"{self.type} - {self.notifiable_type} - {self.created_at}"

class Chat(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_chats')
    support_chat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='participated_chats'
    )

    class Meta:
        db_table = 'chats'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['support_chat']),
        ]

    def __str__(self):
        return f"Chat with {self.user.get_full_name()} ({'Support' if self.support_chat else 'Regular'})"

class Message(models.Model):
    content = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.time and not self.id:
            self.time = timezone.now().time()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['chat', 'created_at']),
        ]

    def __str__(self):
        return f"Message from {self.sender} at {self.created_at}"

class UserPresence(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='presence')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_presences'
        verbose_name_plural = 'User presences'

    def __str__(self):
        return f"{self.user.username}'s presence - {'Online' if self.is_online else 'Offline'}"

def process_and_save_data(raw_data):
    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    for item in raw_data:
        print(f"Processing item: {item}")  # Log the item to understand its structure
        if not isinstance(item, dict):
            print(f"Unexpected item format: {item}")
            continue
        # Existing processing logic...

class Bill(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bills')
    bill_num = models.CharField(max_length=255, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    receipt_num = models.CharField(max_length=255, null=True, blank=True)
    receipt_upload = models.FileField(upload_to='receipts/%Y/%m/%d/', null=True, blank=True)
    receipt_createat = models.DateTimeField(null=True, blank=True)
    receipt_verified = models.BooleanField(default=False)
    receipt_verifiedby = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='verified_bills')
    receipt_verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bills'

    def save(self, *args, **kwargs):
        if not self.bill_num:
            timestamp = int(timezone.now().timestamp())
            self.bill_num = f"{timestamp}{self.user_id}"
        super().save(*args, **kwargs)

class TaskExecution(models.Model):
    task_name = models.CharField(max_length=100)
    last_run = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='success')
    interval = models.IntegerField(default=60)  # seconds

    class Meta:
        get_latest_by = 'last_run'

class ApiKeyUsageLog(models.Model):
    api_key = models.ForeignKey('ApiAccessKey', on_delete=models.CASCADE, related_name='usage_logs')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='api_usage_logs')
    request_path = models.CharField(max_length=255)
    query_params = models.JSONField(null=True, blank=True)
    response_format = models.CharField(
        max_length=10,
        choices=[
            ('json', 'JSON'),
            ('csv', 'CSV'),
            ('xml', 'XML')
        ],
        default='json'
    )
    status_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_key_usage_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['api_key', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.api_key} - {self.request_path} - {self.created_at}"