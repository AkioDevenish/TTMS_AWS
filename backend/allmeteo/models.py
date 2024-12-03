from django.db import models

class WeatherMeasurement(models.Model):
    device_name = models.CharField(max_length=100)
    sensor_name = models.CharField(max_length=100)
    sensor_sn = models.CharField(max_length=100)
    units = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.device_name} - {self.sensor_name}"

class WeatherReading(models.Model):
    measurement = models.ForeignKey(WeatherMeasurement, on_delete=models.CASCADE, related_name="readings")
    value = models.FloatField()
    datetime = models.DateTimeField()
    timestamp_utc = models.DateTimeField()
    precision = models.FloatField(null=True, blank=True)
    error_flag = models.BooleanField(default=False)
    error_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Reading at {self.datetime}: {self.value} {self.measurement.units}"
