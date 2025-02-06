from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    BrandViewSet, StationViewSet, SensorViewSet,
    MeasurementViewSet, StationViewSet, StationHealthLogViewSet,
    StationSensorViewSet, ApiAccessKeyViewSet, SystemLogViewSet,
    UserViewSet, NotificationViewSet, verify_token, get_current_user,
    CustomTokenObtainPairView, MessageListCreate, MessageDetail, ConversationList,
    MarkMessageRead, UserList, LoginView, ChatListCreate, ChatDetail, ChatMessages,
    UserPresenceUpdate, ChatViewSet, MessageViewSet, UserPresenceList
)

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'measurements', MeasurementViewSet)
router.register(r'stations', StationViewSet)
router.register(r'station-health-logs', StationHealthLogViewSet)
router.register(r'station-sensors', StationSensorViewSet)
router.register(r'api-keys', ApiAccessKeyViewSet)
router.register(r'system-logs', SystemLogViewSet)
router.register(r'users', UserViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', verify_token, name='verify_token'),
    path('api/user/me/', get_current_user, name='current_user'),
    path('messages/', MessageListCreate.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),
    path('conversations/<int:user_id>/', ConversationList.as_view(), name='conversation-list'),
    path('messages/mark-read/<int:pk>/', MarkMessageRead.as_view(), name='mark-message-read'),
    path('users/', UserList.as_view(), name='user-list'),
    path('api/chats/', ChatListCreate.as_view(), name='chat-list-create'),
    path('api/chats/<int:pk>/', ChatDetail.as_view(), name='chat-detail'),
    path('api/chats/<int:pk>/messages/', ChatMessages.as_view(), name='chat-messages'),
    path('api/users/<int:user_id>/presence/', UserPresenceUpdate.as_view(), name='user-presence'),
    path('api/user-presences/', UserPresenceList.as_view(), name='user-presence-list'),
]