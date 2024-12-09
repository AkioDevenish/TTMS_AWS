from django.db import models
from database.models import Instrument

class Measurements(models.Model):
    name = models.CharField(max_length=100)
    measurement_name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField()
    is_test = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    instrument = models.ForeignKey(
        Instrument,  
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        related_name='measurements',  
        help_text="The instrument associated with this measurement"
    )

    class Meta:
        db_table = 'paws_measurements'

    def __str__(self):
        return f"{self.name} - {self.measurement_name} - {self.timestamp} - Instrument ID: {self.instrument.id}"
