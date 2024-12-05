from django.db import models

class WeatherMeasurement(models.Model):

    device_name = models.CharField(max_length=100, help_text="Name of the device (e.g., ATMOS 41)")
    sensor_name = models.CharField(max_length=100, help_text="Specific sensor name (e.g., Wind Speed, Air Temperature)")
    sensor_sn = models.CharField(max_length=100, null=True, blank=True, help_text="Serial number of the sensor")
    value = models.FloatField(help_text="Measured value", null=False)  # Ensure value is never null
    units = models.CharField(max_length=50, help_text="Units of the measurement (e.g., °C, mm, m/s)")
    timestamp = models.DateTimeField(help_text="Timestamp of the measurement")
    timestamp_utc = models.DateTimeField(help_text="UTC timestamp of the measurement")
    precision = models.FloatField(null=True, blank=True, help_text="Precision of the measurement (if applicable)")
    error_flag = models.BooleanField(default=False, help_text="Indicates if there was an error during measurement")
    error_description = models.TextField(null=True, blank=True, help_text="Details of any error encountered")

    def __str__(self):
        return f"{self.device_name} - {self.sensor_name}: {self.value} {self.units} at {self.timestamp}"
