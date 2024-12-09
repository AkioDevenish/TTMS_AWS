from django.contrib import admin
from .models import Measurements

@admin.register(Measurements)
class MeasurementsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_name', 'value', 'timestamp', 'is_test', 'created_at', 'updated_at')
    list_filter = ('name', 'measurement_name', 'timestamp')
    search_fields = ('name', 'measurement_name')
