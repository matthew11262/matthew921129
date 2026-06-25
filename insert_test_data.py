#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mainapp.models import SensorData
from django.utils import timezone

# Clear existing data
SensorData.objects.all().delete()

# Add sample sensor data for the last 7 days
now = timezone.now()
for days_back in range(7):
    timestamp = now - timedelta(days=days_back)
    
    for i in range(3):  # 3 readings per day per sensor
        timestamp_offset = timestamp - timedelta(hours=i*8)
        
        SensorData.objects.create(
            sensor_type='temperature',
            value=round(20 + random.uniform(-3, 3), 2),
            timestamp=timestamp_offset,
            is_latest=(days_back == 0 and i == 0),
        )
        
        SensorData.objects.create(
            sensor_type='humidity',
            value=round(60 + random.uniform(-15, 15), 2),
            timestamp=timestamp_offset,
            is_latest=(days_back == 0 and i == 0),
        )
        
        SensorData.objects.create(
            sensor_type='light',
            value=round(500 + random.uniform(-200, 200), 2),
            timestamp=timestamp_offset,
            is_latest=(days_back == 0 and i == 0),
        )

print("✓ Test data inserted successfully!")
print(f"Total records: {SensorData.objects.count()}")
