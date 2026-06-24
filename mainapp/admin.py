from django.contrib import admin
from .models import SensorData

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'value', 'timestamp', 'is_latest')
    list_filter = ('sensor_type', 'is_latest')
    ordering = ('-timestamp',)

