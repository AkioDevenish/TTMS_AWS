# paws/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstrumentMeasurementViewSet

router = DefaultRouter()
router.register(r'instrument_measurements', InstrumentMeasurementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
