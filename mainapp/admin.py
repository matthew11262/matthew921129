from django.contrib import admin
from .models import ButtonData, GameState  # 移除 SensorData，改引入 ButtonData 與新關卡的 GameState

@admin.register(GameState)
class GameStateAdmin(admin.ModelAdmin):
    # 讓後台列表能一眼看清這 9 大關卡的當前數值
    list_display = ('timestamp', 'direction', 'key_height', 'error_count', 'freq', 'rgb_color', 'morse_code', 'vault_knob', 'keypad', 'switch_state', 'is_latest')
    list_filter = ('is_latest',)
    ordering = ('-timestamp',)

@admin.register(ButtonData)
class ButtonDataAdmin(admin.ModelAdmin):
    # 保留你原本外接實體按鈕的後台管理介面
    list_display = ('button_id', 'status', 'timestamp', 'is_latest')
    list_filter = ('status', 'is_latest')
    ordering = ('-timestamp',)