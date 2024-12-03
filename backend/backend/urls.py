from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/allmeteo/', include('allmeteo.urls')),  # Include the allmeteo API
    path('', include('paws.urls')),
]

