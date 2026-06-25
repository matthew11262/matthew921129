import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mainapp.models import ButtonData

# Check latest button with is_latest flag
latest = ButtonData.objects.filter(is_latest=True).first()
print(f"Latest with is_latest=True: {latest}")

# Check most recent button record by timestamp
most_recent = ButtonData.objects.order_by('-timestamp').first()
print(f"Most recent by timestamp: {most_recent}")
print(f"  is_latest: {most_recent.is_latest if most_recent else 'N/A'}")
print(f"  status: {most_recent.status if most_recent else 'N/A'}")

# Count all button records
total = ButtonData.objects.count()
print(f"Total button records: {total}")

# Count is_latest=True
latest_count = ButtonData.objects.filter(is_latest=True).count()
print(f"Records with is_latest=True: {latest_count}")
