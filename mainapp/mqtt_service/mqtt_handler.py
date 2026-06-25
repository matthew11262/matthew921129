import json
from mainapp.models import GameState, ButtonData

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        
        # 處理遊戲狀態 (9 大關卡)
        if topic == 'escaperoom/game_state':
            data = json.loads(payload)
            # 先將舊狀態標記為非最新
            GameState.objects.filter(is_latest=True).update(is_latest=False)
            # 建立新的狀態
            GameState.objects.create(
                direction=data.get('dir'),
                key_height=data.get('key'),
                error_count=data.get('err'),
                freq=data.get('freq'),
                rgb_color=data.get('rgb'),
                morse_code=data.get('morse'),
                vault_knob=data.get('vault'),
                keypad=data.get('keypad'),
                switch_state=data.get('switch'),
                is_latest=True
            )
            print("遊戲狀態已更新")

        # 處理按鈕狀態 (保留你原本的邏輯)
        elif topic == 'escaperoom/button':
            data = json.loads(payload)
            btn_id = data.get('button_id')
            btn_status = data.get('status')
            
            ButtonData.objects.filter(button_id=btn_id, is_latest=True).update(is_latest=False)
            ButtonData.objects.create(
                button_id=btn_id,
                status=btn_status,
                timestamp=timezone.now(),
                is_latest=True
            )
            print(f"按鈕 {btn_id} 狀態已更新")

    except Exception as exc:
        print('MQTT 處理錯誤:', exc)