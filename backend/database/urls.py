from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, InstrumentViewSet

# Initialize the default router
router = DefaultRouter()

# Register Brand and Instrument viewsets with the router
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'instruments', InstrumentViewSet, basename='instrument')

# Include the router's URLs in the application's URL configuration
urlpatterns = [
    path('', include(router.urls)),
]
