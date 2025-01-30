from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Brand, Station, Sensor, Measurement,
    StationHealthLog, StationSensor, ApiAccessKey,
    SystemLog, User, Notification, Message, Chat, UserPresence
)
from .serializers import (
    BrandSerializer, StationSerializer, SensorSerializer,
    MeasurementSerializer, StationSerializer, StationHealthLogSerializer,
    StationSensorSerializer, ApiAccessKeySerializer, SystemLogSerializer,
    UserSerializer, NotificationSerializer, MessageSerializer,
    UserCreateSerializer, LoginSerializer, ChatSerializer, UserPresenceSerializer
)
from django.utils import timezone
from rest_framework import serializers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import timedelta
import datetime
from django.db.models import Q
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

User = get_user_model()

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @action(detail=True, methods=['get'])
    def stations(self, request, pk=None):
        brand = self.get_object()
        stations = brand.stations.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("Received data:", request.data)
            data = request.data.copy()
            if 'last_updated_at' not in data:
                data['last_updated_at'] = timezone.now()

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def measurements(self, request, pk=None):
        station = self.get_object()
        measurements = station.measurements.all()
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def health_logs(self, request, pk=None):
        station = self.get_object()
        logs = station.health_logs.all()
        serializer = StationHealthLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def latest_health(self, request, pk=None):
        station = self.get_object()
        latest_health = station.health_logs.order_by('-created_at').first()
        if latest_health:
            serializer = StationHealthLogSerializer(latest_health)
            return Response(serializer.data)
        return Response({'error': 'No health data available'}, status=404)


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @action(detail=True, methods=['get'])
    def stations(self, request, pk=None):
        sensor = self.get_object()
        stations = sensor.stations.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    @action(detail=False, methods=['get'])
    def by_station(self, request):
        station_id = request.query_params.get('station_id')
        if not station_id:
            return Response({"error": "station_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        measurements = self.queryset.filter(station_id=station_id)
        serializer = self.serializer_class(measurements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_sensor(self, request):
        sensor_id = request.query_params.get('sensor_id')
        if not sensor_id:
            return Response({"error": "sensor_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        measurements = self.queryset.filter(sensor_id=sensor_id)
        serializer = self.serializer_class(measurements, many=True)
        return Response(serializer.data)


class StationHealthLogViewSet(viewsets.ModelViewSet):
    queryset = StationHealthLog.objects.all()
    serializer_class = StationHealthLogSerializer

    @action(detail=False, methods=['get'])
    def by_station(self, request):
        station_id = request.query_params.get('station_id')
        if not station_id:
            return Response({"error": "station_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        logs = self.queryset.filter(station_id=station_id)
        serializer = self.serializer_class(logs, many=True)
        return Response(serializer.data)


class StationSensorViewSet(viewsets.ModelViewSet):
    queryset = StationSensor.objects.all()
    serializer_class = StationSensorSerializer


class ApiAccessKeyViewSet(viewsets.ModelViewSet):
    queryset = ApiAccessKey.objects.all()
    serializer_class = ApiAccessKeySerializer


class SystemLogViewSet(viewsets.ModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer

    @action(detail=False, methods=['get'])
    def by_module(self, request):
        module = request.query_params.get('module')
        if not module:
            return Response({"error": "module is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        logs = self.queryset.filter(module=module)
        serializer = self.serializer_class(logs, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Prevent deleting yourself
            if instance.id == request.user.id:
                return Response(
                    {"error": "You cannot delete your own account"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Only superusers can delete other users
            if not request.user.is_superuser:
                return Response(
                    {"error": "Only superusers can delete users"},
                    status=status.HTTP_403_FORBIDDEN
                )
            self.perform_destroy(instance)
            return Response(
                {"message": "User deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Debug print
        print("Received data:", data)

        # Validate expires_at format
        if 'expires_at' in data and data['expires_at']:
            try:
                # Ensure date is in correct format
                datetime.datetime.strptime(data['expires_at'], '%Y-%m-%d')
            except ValueError:
                return Response(
                    {"error": "Invalid date format for expires_at. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def presence(self, request, pk=None):
        if int(pk) != request.user.id:
            return Response(
                {"error": "Cannot update other user's presence"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            user_presence, _ = UserPresence.objects.get_or_create(user_id=pk)
            user_presence.is_online = request.data.get('is_online', False)
            user_presence.save()
            
            return Response({
                'id': pk,
                'is_online': user_presence.is_online,
                'last_seen': user_presence.last_seen
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=False, methods=['get'])
    def unread(self, request):
        notifications = self.queryset.filter(read_at__isnull=True)
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read_at = timezone.now()
        notification.save()
        serializer = self.serializer_class(notification)
        return Response(serializer.data)

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'stations', StationViewSet)
router.register(r'station-health-logs', StationHealthLogViewSet)
router.register(r'station-sensors', StationSensorViewSet)
router.register(r'api-tokens', ApiAccessKeyViewSet)
router.register(r'system-logs', SystemLogViewSet)
router.register(r'users', UserViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    return Response({'valid': True})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_user(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        })
    return Response({'detail': 'Not authenticated'}, status=401)

@api_view(['GET'])
def get_latest_timestamp(request):
    latest_measurement = Measurement.objects.order_by('-date', '-time').first()
    if latest_measurement:
        timestamp = f"{latest_measurement.date}T{latest_measurement.time}"
        return Response({'timestamp': timestamp})
    return Response({'timestamp': None}, status=404)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class MessageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            Q(chat__user=self.request.user) | Q(sender=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class ConversationList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user = self.kwargs['user_id']
        return Message.objects.filter(
            Q(chat__user_id=other_user, sender=self.request.user) |
            Q(chat__user=self.request.user, sender_id=other_user)
        ).order_by('created_at')

class MarkMessageRead(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.recipient == request.user and not message.read_at:
            message.read_at = timezone.now()
            message.save()
        return Response(self.get_serializer(message).data)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all().order_by('-created_at')

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'role': user.role,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            })
        return Response(serializer.errors, status=401)

class ChatListCreate(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        support_chat = self.request.query_params.get('support_chat', False)

        queryset = Chat.objects.all()
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if support_chat:
            queryset = queryset.filter(support_chat=True)
        return queryset

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

class ChatMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        return Message.objects.filter(chat_id=chat_id)

class UserPresenceUpdate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"error": "User not authenticated"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Then check if user is updating their own presence
        if request.user.id != user_id:
            return Response(
                {"error": "Cannot update other user's presence"}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            user_presence, _ = UserPresence.objects.get_or_create(user_id=user_id)
            user_presence.is_online = request.data.get('is_online', False)
            user_presence.save()
            
            return Response({
                'id': user_id,
                'is_online': user_presence.is_online,
                'last_seen': user_presence.last_seen
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)