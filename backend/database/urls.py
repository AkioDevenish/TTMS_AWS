from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    BrandViewSet,
    StationViewSet,
    SensorViewSet,
    MeasurementViewSet,
    StationHealthLogViewSet,
    StationSensorViewSet,
    ApiAccessKeyViewSet,
    SystemLogViewSet,
    UserViewSet,
    NotificationViewSet,
    verify_token,
    get_current_user,
    CustomTokenObtainPairView,
    MessageListCreate,
    MessageDetail,
    ConversationList,
    MarkMessageRead,
    UserList,
    LoginView,
    ChatListCreate,
    ChatDetail,
    ChatMessages,
    ChatViewSet,
    MessageViewSet,
    BillViewSet,
    HistoricalDataViewSet,
    ApiKeyUsageLogViewSet,
    get_user_api_keys,
    get_task_execution_status,
    get_task_status,
    get_stations_status,
    get_stations_comprehensive_status,
    inactive_sensors,
    aws_station_health_logs,
    PlanViewSet,
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r"brands", BrandViewSet)
router.register(r"sensors", SensorViewSet)
router.register(r"measurements", MeasurementViewSet, basename="measurement")
router.register(r"stations", StationViewSet, basename="station")
router.register(r"station-health-logs", StationHealthLogViewSet)
router.register(r"station-sensors", StationSensorViewSet)
router.register(r"api-keys", ApiAccessKeyViewSet)
router.register(r"system-logs", SystemLogViewSet)
router.register(r"users", UserViewSet)
router.register(r"notifications", NotificationViewSet)
router.register(r"chats", ChatViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"bills", BillViewSet)
router.register(r"historical-data", HistoricalDataViewSet, basename="historical-data")
router.register(r"api-key-usage-logs", ApiKeyUsageLogViewSet)
router.register(r"plans", PlanViewSet)

urlpatterns = [
    # Custom endpoints must come BEFORE the router to avoid conflicts
    path("api/stations/status/", get_stations_status, name="stations-status"),
    path(
        "api/stations/comprehensive-status/",
        get_stations_comprehensive_status,
        name="stations-comprehensive-status",
    ),
    path(
        "api/stations/aws-health/", aws_station_health_logs, name="aws-station-health"
    ),
    path(
        "api/measurements/inactive_sensors/", inactive_sensors, name="inactive_sensors"
    ),
    path(
        "api/task-execution-status/",
        get_task_execution_status,
        name="task-execution-status",
    ),
    path("api/task-status/", get_task_status, name="task-status"),
    # Router URLs (these come after custom endpoints)
    path("api/", include(router.urls)),
    # Other endpoints
    path("api/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/verify/", verify_token, name="verify_token"),
    path("api/user/me/", get_current_user, name="current_user"),
    path("messages/", MessageListCreate.as_view(), name="message-list-create"),
    path("messages/<int:pk>/", MessageDetail.as_view(), name="message-detail"),
    path(
        "conversations/<int:user_id>/",
        ConversationList.as_view(),
        name="conversation-list",
    ),
    path(
        "messages/mark-read/<int:pk>/",
        MarkMessageRead.as_view(),
        name="mark-message-read",
    ),
    path("users/", UserList.as_view(), name="user-list"),
    path("api/chats/", ChatListCreate.as_view(), name="chat-list-create"),
    path("api/chats/<int:pk>/", ChatDetail.as_view(), name="chat-detail"),
    path("api/chats/<int:pk>/messages/", ChatMessages.as_view(), name="chat-messages"),
    path("user/api-keys/", get_user_api_keys, name="user-api-keys"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
