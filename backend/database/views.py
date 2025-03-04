from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Brand, Station, Sensor, Measurement,
    StationHealthLog, StationSensor, ApiAccessKey,
    SystemLog, User, Notification, Message, Chat, UserPresence, Bill, TaskExecution
)
from .serializers import (
    BrandSerializer, StationSerializer, SensorSerializer,
    MeasurementSerializer, StationSerializer, StationHealthLogSerializer,
    StationSensorSerializer, ApiAccessKeySerializer, SystemLogSerializer,
    UserSerializer, NotificationSerializer, MessageSerializer,
    UserCreateSerializer, LoginSerializer, ChatSerializer, UserPresenceSerializer,
    BillSerializer
)
from django.utils import timezone
from rest_framework import serializers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import timedelta, timezone as tz
import datetime
from django.db.models import Q
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from django.http import HttpResponse
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

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
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]  # Only admins can update/delete
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
        
        # Validate expires_at format
        if 'expires_at' in data and data['expires_at']:
            try:
                # Parse the date and set it to end of day in UTC
                date = datetime.datetime.strptime(data['expires_at'], '%Y-%m-%d')
                date = date.replace(hour=23, minute=59, second=59)
                # Convert to UTC timezone-aware datetime
                data['expires_at'] = timezone.make_aware(date, tz.utc)
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

    @action(detail=True, methods=['get', 'post'])
    def presence(self, request, pk=None):
        if request.method == 'POST':
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
        else:  # GET request
            presences = UserPresence.objects.all()
            serializer = UserPresenceSerializer(presences, many=True)
            return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # If status is being updated
            if 'status' in request.data:
                # Only superusers can change status
                if not request.user.is_superuser:
                    return Response(
                        {"error": "Only administrators can modify user status"},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Prevent self-suspension
                if instance.id == request.user.id:
                    return Response(
                        {"error": "You cannot modify your own status"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Update the status
                new_status = request.data['status']
                if new_status not in [choice[0] for choice in User.STATUS_CHOICES]:
                    return Response(
                        {"error": "Invalid status value"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                instance.status = new_status
                instance.save(update_fields=['status'])
                
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            
            return Response(
                {"error": "No status provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
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
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # If support user, get all users except support
        if self.request.user.email == 'mdpssupport@metoffice.gov.tt':
            return User.objects.exclude(email='mdpssupport@metoffice.gov.tt').order_by('-created_at')
        # For regular users, only get support user
        return User.objects.filter(email='mdpssupport@metoffice.gov.tt')

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                
                # Double-check suspension and inactive status
                if user.status == 'Suspended':
                    return Response(
                        {'error': 'Your account has been suspended. Please contact support.'},
                        status=403
                    )
                elif user.status == 'Inactive':
                    return Response(
                        {'error': 'Your account has expired. Please renew your subscription.'},
                        status=403
                    )
                
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
                        'is_superuser': user.is_superuser,
                        'status': user.status
                    }
                })
            return Response(serializer.errors, status=401)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class ChatListCreate(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # If support user, get all chats
        if user.email == 'mdpssupport@metoffice.gov.tt':
            return Chat.objects.all()\
                .select_related('user')\
                .prefetch_related('messages', 'participants')\
                .order_by('-created_at')
        
        # For regular users, get their chats with support
        return Chat.objects.filter(
            Q(user=user) | 
            Q(participants=user) |
            Q(support_chat=True)
        ).select_related('user')\
         .prefetch_related('messages', 'participants')\
         .order_by('-created_at')

    def perform_create(self, serializer):
        chat = serializer.save(user=self.request.user)
        # Add both users as participants
        chat.participants.add(self.request.user)
        
        # If this is a support chat, add the support user as participant
        if self.request.data.get('support_chat'):
            support_user = User.objects.get(email='mdpssupport@metoffice.gov.tt')
            chat.participants.add(support_user)

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

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(
            Q(user=self.request.user) | 
            Q(participants=self.request.user)
        ).distinct()

    def create(self, request, *args, **kwargs):
        try:
            print("Creating chat with data:", request.data)
            
            # Check if a chat already exists
            other_user_id = request.data.get('user_id')
            if other_user_id:
                existing_chat = Chat.objects.filter(
                    Q(user=request.user, participants__id=other_user_id) |
                    Q(user_id=other_user_id, participants=request.user)
                ).first()
                
                if existing_chat:
                    print(f"Found existing chat: {existing_chat.id}")
                    return Response(self.get_serializer(existing_chat).data)

            # Create new chat without user in request data
            chat_data = request.data.copy()
            chat_data.pop('user_id', None)  # Remove user_id from data
            
            serializer = self.get_serializer(data=chat_data)
            serializer.is_valid(raise_exception=True)
            
            # Save without committing to add participants
            chat = serializer.save()
            
            # Add participants
            chat.participants.add(request.user)
            if other_user_id:
                chat.participants.add(other_user_id)
            
            print(f"Created new chat: {chat.id}")
            return Response(serializer.data, status=201)
            
        except Exception as e:
            print(f"Error creating chat: {str(e)}")
            return Response({"error": str(e)}, status=400)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            Q(chat__user=self.request.user) | 
            Q(sender=self.request.user)
        ).select_related('sender', 'chat')

    def create(self, request, *args, **kwargs):
        print("Received message data:", request.data)  # Debug print
        
        try:
            chat_id = request.data.get('chat')
            if not chat_id:
                return Response({"error": "Chat ID is required"}, status=400)
                
            chat = get_object_or_404(Chat, id=chat_id)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            message = serializer.save(
                chat=chat,
                sender=request.user,
                time=timezone.now().time()
            )
            
            print(f"Message created: {message.id}")  # Debug print
            return Response(serializer.data, status=201)
            
        except Exception as e:
            print(f"Error creating message: {str(e)}")  # Debug print
            return Response({"error": str(e)}, status=400)

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        
        if self.request.user.is_staff:
            if user_id:
                return Bill.objects.filter(user_id=user_id)
            return Bill.objects.all()
        
        # Regular users can only see their own bills
        return Bill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def verify_receipt(self, request, pk=None):
        if not request.user.is_staff:
            raise PermissionDenied("Only staff can verify receipts")
        
        bill = self.get_object()
        bill.receipt_verified = True
        bill.receipt_verifiedby = request.user
        bill.receipt_verified_at = timezone.now()
        bill.save()
        
        return Response({'status': 'receipt verified'})

    @action(detail=True, methods=['POST'])
    def upload_receipt(self, request, pk=None):
        bill = self.get_object()
        if 'receipt_upload' not in request.FILES:
            return Response({'error': 'No receipt file provided'}, status=400)
        
        bill.receipt_upload = request.FILES['receipt_upload']
        bill.receipt_createat = timezone.now()
        # Generate receipt number using timestamp and user_id
        timestamp = int(timezone.now().timestamp())
        bill.receipt_num = f"RCP{timestamp}{bill.user_id}"
        # Set verification details
        bill.receipt_verified = True
        bill.receipt_verifiedby = request.user
        bill.receipt_verified_at = timezone.now()
        bill.save()
        
        return Response({
            'message': 'Receipt uploaded successfully',
            'receipt_url': bill.receipt_upload.url if bill.receipt_upload else None,
            'receipt_num': bill.receipt_num,
            'verified_by': request.user.email,
            'verified_at': bill.receipt_verified_at
        })

    @action(detail=True, methods=['GET'])
    def receipt_upload(self, request, pk=None):
        bill = self.get_object()
        if not bill.receipt_upload:
            return Response({'error': 'No receipt found'}, status=404)
        
        # Get file extension
        file_name = bill.receipt_upload.name.lower()
        if file_name.endswith('.pdf'):
            content_type = 'application/pdf'
        elif file_name.endswith(('.png', '.jpg', '.jpeg')):
            content_type = f'image/{file_name.split(".")[-1]}'
        else:
            content_type = 'application/octet-stream'
        
        response = HttpResponse(bill.receipt_upload.read(), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{bill.receipt_upload.name}"'
        return response

@api_view(['GET'])
@permission_classes([AllowAny])
def get_task_execution_status(request):
    try:
        tasks = TaskExecution.objects.all().order_by('task_name')
        current_time = timezone.now()
        
        task_statuses = []
        for task in tasks:
            time_since_last_run = 0
            if task.last_run:
                time_since_last_run = (current_time - task.last_run).total_seconds()
            
            # Calculate time until next run
            time_until_next = max(0, task.interval - (time_since_last_run % task.interval))
            
            # Calculate progress percentage
            progress = min(100, (time_since_last_run % task.interval) / task.interval * 100)
            
            task_statuses.append({
                'id': task.id,
                'name': task.task_name,
                'brand': task.task_name.replace('_', ' ').title(),
                'status': task.status,
                'last_updated': task.last_run,
                'time_until_next': time_until_next,
                'progress': progress
            })
        
        return Response(task_statuses)
    except Exception as e:
        logger.error(f"Error getting task execution status: {str(e)}")
        return Response({'error': str(e)}, status=500)

# Alias for backward compatibility
get_task_status = get_task_execution_status

@api_view(['GET'])
@permission_classes([AllowAny])
def get_stations_status(request):
    try:
        stations = Station.objects.all().select_related('brand')
        current_time = timezone.now()
        
        station_statuses = []
        for station in stations:
            # Get latest health log
            latest_health = station.health_logs.order_by('-created_at').first()
            
            # Calculate time until next update based on brand
            interval = 3600 if station.brand.name == '3D_Paws' else 60
            time_since_last = 0
            if latest_health:
                time_since_last = (current_time - latest_health.created_at).total_seconds()
            
            time_until_next = max(0, interval - (time_since_last % interval))
            progress = min(100, (time_since_last % interval) / interval * 100)
            
            station_statuses.append({
                'id': station.id,
                'name': station.name,
                'brand': station.brand.name,
                'status': latest_health.connectivity_status if latest_health else 'Unknown',
                'last_updated': latest_health.created_at if latest_health else None,
                'time_until_next': time_until_next,
                'progress': progress
            })
        
        return Response(station_statuses)
    except Exception as e:
        logger.error(f"Error getting stations status: {str(e)}")
        return Response({'error': str(e)}, status=500)
