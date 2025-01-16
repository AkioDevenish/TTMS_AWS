from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Brand, Station, Sensor, Measurement,
    StationHealthLog, StationSensor, APIAccessToken,
    SystemLog, User, Notification
)

# Register your models
admin.site.register(Brand)
admin.site.register(Station)
admin.site.register(Sensor)
admin.site.register(Measurement)
admin.site.register(StationHealthLog)
admin.site.register(StationSensor)
admin.site.register(APIAccessToken)
admin.site.register(SystemLog)
admin.site.register(User)
admin.site.register(Notification)