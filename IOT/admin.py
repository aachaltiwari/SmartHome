from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import urlencode, format_html

from.import models


# Register your models here.
class UserProfileInline(admin.TabularInline):
    model = models.UserProfile

class RFIDInline(admin.TabularInline):
    model = models.RFID

class WifiInline(admin.TabularInline):
    model = models.Wifi

class RoomInline(admin.TabularInline):
    model = models.Room
    extra = 1

class SensorInline(admin.TabularInline):
    model = models.Sensor
    extra = 1

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline, RFIDInline, WifiInline, RoomInline, SensorInline]
    list_display = ['id', 'username', 'user_profile', 'rfid', 'wifi_detail', 'sensors', 'rooms', 'notifications']
    list_select_related = ['userprofile', 'rfid', 'wifi']
    ordering = ['id']
    search_fields = ['username__istartswith']

    def user_profile(self, user):
        url = reverse('admin:IOT_userprofile_changelist')+ '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href = "{}">Profile</a>', url)

    def wifi_detail(self, user):
        url = reverse('admin:IOT_wifi_changelist')+ '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href = "{}">{}</a>', url, user.wifi.wifi_ssid)

    def sensors(self, user):   
        url = reverse('admin:IOT_sensor_changelist')+ '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href = "{}">{}</a>', url, user.sensors)
    
    def rooms(self, user):   
        url = reverse('admin:IOT_room_changelist')+ '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href = "{}">{}</a>', url, user.rooms)
    
    def notifications(self, user):   
        url = reverse('admin:IOT_notification_changelist')+ '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href = "{}">{}</a>', url, user.notifications)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
        sensors = Count('sensor', distinct=True),
        rooms = Count('room', distinct=True),
        notifications = Count('notification', distinct=True)
        )
    


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'phone_no']
    list_editable = ['phone_no']
    list_filter = ['user']
    list_select_related = ['user']
    ordering = ['user']
    search_fields = ['phone_no__istartswith', 'user__istartwith']



@admin.register(models.RFID)
class RFIDAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'door_status']
    list_select_related = ['user']
    ordering = ['user']



@admin.register(models.Wifi)
class WifiAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'wifi_ssid', 'wifi_password']
    list_editable = ['wifi_ssid', 'wifi_password']
    list_filter = ['user']
    list_select_related = ['user']
    ordering = ['user']
    search_fields = ['wifi_ssid__istartswith']
    
    

@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['id', 'name', 'text', 'user']
    list_select_related = ['user']
    list_filter = ['user']
    ordering = ['id']
    search_fields = ['name__istartswith']
 


class BulbInline(admin.TabularInline):
    model = models.Bulb
    extra = 1
    
    
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    inlines = [BulbInline]
    list_display = ['id', 'name', 'user', 'bulbs']
    list_filter = ['user']
    list_select_related = ['user']
    ordering = ['id']
    search_fields = ['name__istartswith']
    
    def bulbs(self, room):   
        url = reverse('admin:IOT_bulb_changelist')+ '?' + urlencode({'room__id': str(room.id)})
        return format_html('<a href = "{}">{}</a>', url, room.bulbs)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
        bulbs = Count('bulb', distinct=True)
        )
    


@admin.register(models.Bulb)
class BulbAdmin(admin.ModelAdmin):
    autocomplete_fields = ['room']
    list_display = ['id', 'colour', 'bulb_status', 'user', 'room']
    list_editable = ['colour']
    list_filter = ['room__user', 'room']
    list_select_related = ['room', 'room__user']
    ordering = ['id']
    search_fields = ['colour__istartswith']
    
    def user(self, obj):
        return obj.room.user.username if obj.room.user else ''



@admin.register(models.Sensor)
class SensorAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['id', 'name', 'value', 'user', 'sensor_values']
    list_filter = ['user']
    list_select_related = ['user']
    ordering = ['id']
    search_fields = ['name__istartswith']
    
    def sensor_values(self, sensor):
        url = reverse('admin:IOT_sensorvaluestore_changelist')+ '?' + urlencode({'sensor__id': str(sensor.id)})
        return format_html('<a href = "{}">{}</a>', url, sensor.sensor_values)
    
    def get_queryset(self, request): 
        return super().get_queryset(request).annotate(
        sensor_values = Count('sensorvaluestore', distinct=True))



@admin.register(models.SensorValueStore)
class SensorValueStoreAdmin(admin.ModelAdmin):
    autocomplete_fields = ['sensor']
    list_display = ['id', 'value', 'date', 'user_name', 'sensor']
    list_filter = ['sensor']
    list_select_related = ['sensor', 'sensor__user']
    ordering = ['id']
    
    def user_name(self,obj):
        return obj.sensor.user.username if obj.sensor.user else ''