from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Brand, Station, Sensor, Measurement,
    StationHealthLog, StationSensor, ApiAccessKey,
    SystemLog, User, Notification, Chat, Message, UserPresence, Bill
)

# Register your models
admin.site.register(Brand)
admin.site.register(Station)
admin.site.register(Sensor)
admin.site.register(Measurement)
admin.site.register(StationHealthLog)
admin.site.register(StationSensor)
admin.site.register(ApiAccessKey)
admin.site.register(SystemLog)
admin.site.register(User)
admin.site.register(Notification)   

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'support_chat', 'created_at')
    list_filter = ('support_chat', 'created_at')
    search_fields = ('name', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'chat', 'sender', 'created_at', 'read_at')
    list_filter = ('chat', 'sender', 'created_at')
    search_fields = ('content', 'sender__username')
    date_hierarchy = 'created_at'

@admin.register(UserPresence)
class UserPresenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_online', 'last_seen')
    list_filter = ('is_online',)

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_num', 'user', 'total', 'package', 'created_at', 'receipt_verified')
    list_filter = ('package', 'receipt_verified', 'created_at')
    search_fields = ('bill_num', 'user__email', 'package')
    date_hierarchy = 'created_at'
