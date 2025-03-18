from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from database.views import get_task_execution_status, get_task_status, get_stations_status, inactive_sensors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/measurements/inactive_sensors/', inactive_sensors, name='inactive_sensors'),
    path('', include('database.urls')),
    path('api/task-execution-status/', get_task_execution_status, name='task-execution-status'),
    path('api/task-status/', get_task_status, name='task-status'),
    path('api/stations/status/', get_stations_status, name='stations-status'),
]