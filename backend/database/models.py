from django.db import models
import json

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True) 

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.name


class Station(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="stations"
    )
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    last_updated_at = models.DateTimeField() 
    address = models.TextField()
    lat_lng = models.CharField(max_length=255, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    installation_date = models.DateField()

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


class Measurement(models.Model):
    station = models.ForeignKey(
        'Station',
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='measurements',
        null=True,
        blank=True
    )
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
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='health_logs'
    )
    battery_status = models.CharField(max_length=50)
    connectivity_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'station_health_logs'

    def __str__(self):
        return f"{self.station} - {self.created_at}"


class StationSensor(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='station_sensors'
    )
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='station_sensors'
    )

    class Meta:
        db_table = 'station_sensors'
        unique_together = ('station', 'sensor')

    def __str__(self):
        return f"{self.station} - {self.sensor}"


class APIAccessToken(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
    last_used = models.DateTimeField(null=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_access_tokens'

    def __str__(self):
        return self.name


class SystemLog(models.Model):
    module = models.CharField(max_length=100)
    activity = models.TextField()
    user_id = models.IntegerField(null=True)
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_logs'

    def __str__(self):
        return f"{self.module} - {self.type} - {self.created_at}"


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} ({self.email})"


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
