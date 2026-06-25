import os
import sys
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mainapp.models import ButtonData
from django.utils import timezone

# Clear existing button data
ButtonData.objects.all().delete()

# Add sample button data for the last 7 days
now = timezone.now()
statuses = ['ON', 'OFF']

for days_back in range(7):
    timestamp = now - timedelta(days=days_back)
    
    for i in range(4):  # 4 readings per day
        timestamp_offset = timestamp - timedelta(hours=i*6)
        status = random.choice(statuses)
        
        ButtonData.objects.create(
            button_id='button_1',
            status=status,
            timestamp=timestamp_offset,
            is_latest=(days_back == 0 and i == 0),
        )

print("✓ Button test data inserted successfully!")
print(f"Total button records: {ButtonData.objects.count()}")
