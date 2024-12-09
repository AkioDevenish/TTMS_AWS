# paws/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeasurementsViewSet

router = DefaultRouter()
router.register(r'Measurements', MeasurementsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
