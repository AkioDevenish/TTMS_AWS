# paws/models.py
from django.db import models

class InstrumentMeasurement(models.Model):
    # Assuming these fields are required
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    measurement_name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField()
    is_test = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.measurement_name} - {self.timestamp}"
