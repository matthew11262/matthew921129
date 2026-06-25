from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import SensorData, ButtonData

HOME_INFO = {
    'name': '謝秉修',
    'student_id': 'B11113027',
    'team_url': 'http://100.97.224.8:8000',
}


def home(request):
    return render(request, 'mainapp/dashboard.html', HOME_INFO)


def api_latest(request):
    latest_values = {}
    for sensor_type in [SensorData.TEMPERATURE, SensorData.HUMIDITY, SensorData.LIGHT]:
        reading = SensorData.objects.filter(sensor_type=sensor_type, is_latest=True).order_by('-timestamp').first()
        if reading:
            latest_values[sensor_type] = {
                'value': reading.value,
                'timestamp': reading.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
        else:
            latest_values[sensor_type] = {
                'value': None,
                'timestamp': None,
            }
    return JsonResponse({'latest': latest_values})


def api_history(request):
    days = int(request.GET.get('days', 7))
    end_time = timezone.now()
    start_time = end_time - timezone.timedelta(days=days)
    readings = SensorData.objects.filter(timestamp__range=(start_time, end_time)).order_by('timestamp')

    timestamps = [r.timestamp.strftime('%Y-%m-%d %H:%M:%S') for r in readings]
    history = {
        'temperature': [r.value for r in readings if r.sensor_type == SensorData.TEMPERATURE],
        'humidity': [r.value for r in readings if r.sensor_type == SensorData.HUMIDITY],
        'light': [r.value for r in readings if r.sensor_type == SensorData.LIGHT],
    }
    return JsonResponse({'history': history, 'timestamps': timestamps})


def api_records(request):
    sensor_type = request.GET.get('type')
    page_number = request.GET.get('page', 1)

    records = SensorData.objects.all()
    if sensor_type in [SensorData.TEMPERATURE, SensorData.HUMIDITY, SensorData.LIGHT]:
        records = records.filter(sensor_type=sensor_type)

    start_date = request.GET.get('date_from')
    end_date = request.GET.get('date_to')
    if start_date:
        records = records.filter(timestamp__date__gte=start_date)
    if end_date:
        records = records.filter(timestamp__date__lte=end_date)

    paginator = Paginator(records, 30)
    page = paginator.get_page(page_number)
    data = [
        {
            'sensor_type': r.sensor_type,
            'value': r.value,
            'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for r in page.object_list
    ]

    return JsonResponse({
        'records': data,
        'page': page.number,
        'num_pages': paginator.num_pages,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
    })


def api_button_status(request):
    latest_button = ButtonData.objects.filter(is_latest=True).order_by('-timestamp').first()
    if latest_button:
        return JsonResponse({
            'button_id': latest_button.button_id,
            'status': latest_button.status,
            'timestamp': latest_button.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return JsonResponse({
        'button_id': None,
        'status': 'UNKNOWN',
        'timestamp': None,
    })


def api_button_history(request):
    days = int(request.GET.get('days', 7))
    end_time = timezone.now()
    start_time = end_time - timezone.timedelta(days=days)
    records = ButtonData.objects.filter(timestamp__range=(start_time, end_time)).order_by('timestamp')

    data = [
        {
            'button_id': r.button_id,
            'status': r.status,
            'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for r in records
    ]
    return JsonResponse({'records': data})
