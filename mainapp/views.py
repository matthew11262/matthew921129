from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import ButtonData, GameState  # 刪除了 SensorData，加入了新關卡的 GameState

HOME_INFO = {
    'name': '謝秉修',
    'student_id': 'B11113027',
    'team_url': 'http://100.97.224.8:8000',
}


def home(request):
    return render(request, 'mainapp/dashboard.html', HOME_INFO)


def api_latest(request):
    """
    獲取最新 9 大關卡的即時遊戲狀態，供前端網頁分開顯示
    """
    reading = GameState.objects.filter(is_latest=True).order_by('-timestamp').first()
    if reading:
        latest_values = {
            'direction': reading.direction,
            'key_height': reading.key_height,
            'error_count': reading.error_count,
            'freq': reading.freq,
            'rgb_color': reading.rgb_color,
            'morse_code': reading.morse_code,
            'vault_knob': reading.vault_knob,
            'keypad': reading.keypad,
            'switch_state': reading.switch_state,
            'timestamp': reading.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
    else:
        latest_values = {
            'direction': '--', 'key_height': '--', 'error_count': '--',
            'freq': '--', 'rgb_color': '--', 'morse_code': '--',
            'vault_knob': '--', 'keypad': '--', 'switch_state': '--',
            'timestamp': None
        }
    return JsonResponse({'latest': latest_values})


def api_history(request):
    """
    原本用於溫濕度折線圖。因數據已移除，回傳空結構避免前端 JS 查無路徑噴 500 錯誤
    """
    return JsonResponse({'history': {}, 'timestamps': []})


def api_records(request):
    """
    分頁讀取 9 大關卡的歷史紀錄資料表格
    """
    page_number = request.GET.get('page', 1)
    records = GameState.objects.all().order_by('-timestamp')

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
            'direction': r.direction,
            'key_height': r.key_height,
            'error_count': r.error_count,
            'freq': r.freq,
            'rgb_color': r.rgb_color,
            'morse_code': r.morse_code,
            'vault_knob': r.vault_knob,
            'keypad': r.keypad,
            'switch_state': r.switch_state,
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


# ==========================================
#  以下為你原本保留、仍在使用的按鈕 (ButtonData) 邏輯
# ==========================================

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